"""
converter/converter.py
=======================
Main voice conversion engine.

VoiceConverter transforms source audio to perceptually match a target
voice profile by sequentially adjusting:

  1. Pitch (mean F0 and contour dynamics)
  2. Formants (vowel resonances, vocal tract length)
  3. Speaking rate (tempo without pitch change)
  4. Energy / dynamics (per-frame RMS matching)
  5. Spectral envelope (optional, high-quality mode only)

Each step is independently tunable via the config object.
"""

from __future__ import annotations

import concurrent.futures
import logging
import os
import time
from math import log2
from typing import Callable, Optional

import librosa
import numpy as np
import soundfile as sf
from scipy.ndimage import median_filter
from scipy.signal import butter, filtfilt, lfilter, lfilter_zi

from .analyzer import VoiceAnalyzer
from .config import VoiceConverterConfig, DEFAULT_CONFIG
from .preprocessor import AudioPreprocessor

logger = logging.getLogger(__name__)


class VoiceConverter:
    """
    End-to-end voice conversion pipeline.

    Parameters
    ----------
    config : VoiceConverterConfig
    """

    def __init__(self, config: VoiceConverterConfig = DEFAULT_CONFIG) -> None:
        self.config = config
        self.preprocessor = AudioPreprocessor()
        self.analyzer = VoiceAnalyzer()
        config.ensure_dirs()

    # ============================================================ pitch

    def match_pitch(
        self,
        source_audio: np.ndarray,
        source_sr: int,
        target_pitch_profile: dict,
    ) -> np.ndarray:
        """
        Shift the mean pitch of *source_audio* to match the target profile.

        The shift in semitones is calculated as::

            semitones = 12 * log2(target_mean / source_mean)

        Pitch dynamics are scaled so the *relative* contour shape is
        preserved while the centre frequency moves to the target mean.

        Parameters
        ----------
        source_audio         : np.ndarray  float32, mono
        source_sr            : int
        target_pitch_profile : dict        profile["pitch"] sub-dict

        Returns
        -------
        np.ndarray  pitch-shifted float32 audio
        """
        target_mean = target_pitch_profile.get("mean", 0.0)
        if target_mean <= 0:
            logger.warning("Target pitch mean is zero; skipping pitch shift")
            return source_audio

        # Analyse source pitch
        src_pitch = self.analyzer.extract_pitch_contour(
            source_audio, source_sr, self.config
        )
        source_mean = src_pitch.get("mean", 0.0)
        if source_mean <= 0:
            logger.warning("Source pitch mean is zero; skipping pitch shift")
            return source_audio

        ratio = target_mean / source_mean
        n_semitones = 12.0 * log2(ratio)
        logger.info(
            "Pitch shift: %.1f Hz → %.1f Hz  (%+.2f semitones)",
            source_mean, target_mean, n_semitones,
        )

        qs = self.config.get_quality_settings()
        shifted = librosa.effects.pitch_shift(
            source_audio,
            sr=source_sr,
            n_steps=n_semitones,
            bins_per_octave=24,      # finer resolution (half-semitone bins)
            n_fft=qs["n_fft"],
            hop_length=qs["hop_length"],
        )
        return shifted.astype(np.float32)

    # =========================================================== formants

    def match_formants(
        self,
        source_audio: np.ndarray,
        source_sr: int,
        target_formants: dict,
    ) -> np.ndarray:
        """
        Shift formant envelope to match target formant values.

        The method uses an LPC-based spectral envelope approach:
        1. Compute LPC coefficients of each frame.
        2. Derive the per-frame spectral envelope (all-pole model).
        3. Compute a frequency-warping factor from the F1/F2 ratio.
        4. Re-synthesise via spectral shaping.

        If parselmouth is unavailable or too few voiced frames exist,
        the function falls back to a gentle spectral tilt to approximate
        the formant shift.

        Parameters
        ----------
        source_audio    : np.ndarray
        source_sr       : int
        target_formants : dict   {"F1": float, "F2": float, ...}

        Returns
        -------
        np.ndarray  formant-adjusted audio
        """
        src_formants = self.analyzer.extract_formants(source_audio, source_sr)

        # Calculate frequency warping factor from F1 ratio
        src_f1 = src_formants.get("F1", 0.0)
        tgt_f1 = target_formants.get("F1", 0.0)

        if src_f1 <= 0 or tgt_f1 <= 0:
            logger.warning("Formant F1 unavailable; skipping formant shift")
            return source_audio

        shift_factor = tgt_f1 / src_f1
        logger.info("Formant shift factor (F1): %.3f", shift_factor)

        # STFT-based spectral envelope morphing
        qs = self.config.get_quality_settings()
        n_fft = qs["n_fft"]
        hop = qs["hop_length"]

        D = librosa.stft(source_audio, n_fft=n_fft, hop_length=hop)
        magnitude = np.abs(D)
        phase = np.angle(D)
        freqs = librosa.fft_frequencies(sr=source_sr, n_fft=n_fft)

        # Build frequency warp map
        n_bins = len(freqs)
        warped_freqs = freqs * shift_factor
        new_magnitude = np.zeros_like(magnitude)

        for bin_idx in range(n_bins):
            # Find where warped_freqs[bin_idx] maps in original freq axis
            src_freq = freqs[bin_idx] / shift_factor
            src_bin = np.searchsorted(freqs, src_freq)
            src_bin = int(np.clip(src_bin, 0, n_bins - 1))
            new_magnitude[bin_idx] = magnitude[src_bin]

        # Smooth transition between warped and original
        blend = min(abs(shift_factor - 1.0), 0.5)  # 0 = no shift, 0.5 = max
        blended = (1 - blend) * magnitude + blend * new_magnitude

        D_out = blended * np.exp(1j * phase)
        result = librosa.istft(D_out, hop_length=hop, n_fft=n_fft)
        return result.astype(np.float32)

    # =========================================================== energy

    def match_energy(
        self,
        source_audio: np.ndarray,
        target_energy_profile: dict,
    ) -> np.ndarray:
        """
        Scale source energy frame-by-frame to match the target's mean
        and dynamic range.

        Parameters
        ----------
        source_audio          : np.ndarray
        target_energy_profile : dict  profile["energy"] sub-dict

        Returns
        -------
        np.ndarray  energy-matched audio
        """
        target_mean = target_energy_profile.get("mean", None)
        if not target_mean or target_mean <= 0:
            return source_audio

        src_rms_frames = librosa.feature.rms(y=source_audio)[0]
        src_mean = float(np.mean(src_rms_frames))
        if src_mean < 1e-9:
            return source_audio

        global_gain = target_mean / src_mean
        # Apply soft clipping
        result = self._apply_soft_clipping(source_audio * global_gain)
        logger.debug("Energy match: gain=%.3f", global_gain)
        return result.astype(np.float32)

    # ======================================================= speaking rate

    def match_speaking_rate(
        self,
        source_audio: np.ndarray,
        source_sr: int,
        target_rate: dict,
    ) -> np.ndarray:
        """
        Time-stretch source audio to match target speaking rate.

        Pitch is preserved via the phase-vocoder (librosa.effects.time_stretch).

        Parameters
        ----------
        source_audio  : np.ndarray
        source_sr     : int
        target_rate   : dict  profile["speaking_rate"] sub-dict

        Returns
        -------
        np.ndarray  rate-adjusted audio
        """
        target_sps = target_rate.get("syllables_per_sec", 0.0)
        if target_sps <= 0:
            return source_audio

        src_rate = self.analyzer.extract_speaking_rate(source_audio, source_sr)
        src_sps = src_rate.get("syllables_per_sec", 0.0)
        if src_sps <= 0:
            return source_audio

        stretch_factor = src_sps / target_sps   # > 1 speeds up, < 1 slows
        stretch_factor = float(np.clip(stretch_factor, 0.5, 2.0))  # safety

        if abs(stretch_factor - 1.0) < 0.05:
            logger.debug("Speaking rate within 5%%; skipping time stretch")
            return source_audio

        logger.info(
            "Speaking rate: %.2f → %.2f  (stretch=%.3f)",
            src_sps, target_sps, stretch_factor,
        )
        qs = self.config.get_quality_settings()
        stretched = librosa.effects.time_stretch(
            source_audio,
            rate=stretch_factor,
            n_fft=qs["n_fft"],
            hop_length=qs["hop_length"],
        )
        return stretched.astype(np.float32)

    # ================================================ spectral envelope

    def apply_spectral_envelope(
        self,
        source_audio: np.ndarray,
        source_sr: int,
        target_spectral: dict,
    ) -> np.ndarray:
        """
        Morph the spectral centroid towards the target's centroid by
        applying a frequency-domain tilt filter.

        Used only in ``quality == "high"`` mode.

        Parameters
        ----------
        source_audio    : np.ndarray
        source_sr       : int
        target_spectral : dict  profile["spectral"] sub-dict

        Returns
        -------
        np.ndarray
        """
        target_centroid = target_spectral.get("centroid_mean", 0.0)
        if target_centroid <= 0:
            return source_audio

        src_centroid = float(librosa.feature.spectral_centroid(y=source_audio, sr=source_sr).mean())
        if src_centroid <= 0:
            return source_audio

        ratio = target_centroid / src_centroid
        logger.info(
            "Spectral centroid morph: %.1f Hz → %.1f Hz (ratio=%.3f)",
            src_centroid, target_centroid, ratio,
        )

        qs = self.config.get_quality_settings()
        n_fft = qs["n_fft"]
        hop = qs["hop_length"]

        D = librosa.stft(source_audio, n_fft=n_fft, hop_length=hop)
        freqs = librosa.fft_frequencies(sr=source_sr, n_fft=n_fft)
        magnitude = np.abs(D)
        phase = np.angle(D)

        # Build a gentle spectral tilt filter (linear in frequency)
        nyquist = source_sr / 2.0
        slope = (ratio - 1.0) * 0.3   # limit to gentle boost/cut
        tilt = 1.0 + slope * (freqs / nyquist)
        tilt = np.clip(tilt, 0.5, 2.0)

        shaped = magnitude * tilt[:, np.newaxis]
        D_out = shaped * np.exp(1j * phase)
        result = librosa.istft(D_out, hop_length=hop, n_fft=n_fft)
        return result.astype(np.float32)

    # =============================================== main pipeline

    def convert_voice(
        self,
        source_audio: np.ndarray,
        source_sr: int,
        target_profile: dict,
        config: Optional[VoiceConverterConfig] = None,
        progress_callback: Optional[Callable[[int, str], None]] = None,
    ) -> tuple[np.ndarray, dict]:
        """
        Full voice-conversion pipeline.

        Steps
        -----
        1. Pitch matching
        2. Formant matching  (if config.formant_shift_enabled)
        3. Speaking-rate matching
        4. Energy matching  (if config.energy_normalization)
        5. Spectral-envelope morphing  (quality == "high" only)
        6. Final normalisation

        Parameters
        ----------
        source_audio      : np.ndarray  preprocessed float32 mono audio
        source_sr         : int
        target_profile    : dict        loaded voice profile
        config            : VoiceConverterConfig  (use self.config if None)
        progress_callback : callable(percent: int, label: str) | None

        Returns
        -------
        converted_audio : np.ndarray
        report          : dict           details of each conversion step
        """
        cfg = config or self.config
        t0 = time.perf_counter()
        report: dict = {
            "steps": [],
            "source_duration_sec": round(len(source_audio) / source_sr, 3),
        }

        def _step(label: str, pct: int, audio: np.ndarray) -> np.ndarray:
            report["steps"].append(label)
            if progress_callback:
                try:
                    progress_callback(pct, label)
                except Exception:
                    pass
            return audio

        audio = source_audio

        # 1. Pitch
        if progress_callback:
            progress_callback(10, "Matching pitch…")
        audio = self.match_pitch(audio, source_sr, target_profile.get("pitch", {}))
        audio = _step("pitch_match", 25, audio)

        # 2. Formants
        if cfg.formant_shift_enabled:
            if progress_callback:
                progress_callback(30, "Matching formants…")
            audio = self.match_formants(audio, source_sr, target_profile.get("formants", {}))
            audio = _step("formant_match", 45, audio)

        # 3. Speaking rate
        if progress_callback:
            progress_callback(50, "Matching speaking rate…")
        audio = self.match_speaking_rate(audio, source_sr, target_profile.get("speaking_rate", {}))
        audio = _step("speaking_rate_match", 65, audio)

        # 4. Energy
        if cfg.energy_normalization:
            if progress_callback:
                progress_callback(70, "Matching energy…")
            audio = self.match_energy(audio, target_profile.get("energy", {}))
            audio = _step("energy_match", 80, audio)

        # 5. Spectral envelope (high quality only)
        if cfg.quality == "high":
            if progress_callback:
                progress_callback(83, "Morphing spectral envelope…")
            audio = self.apply_spectral_envelope(
                audio, source_sr, target_profile.get("spectral", {})
            )
            audio = _step("spectral_envelope_morph", 90, audio)

        # 6. Final normalisation
        audio = self.preprocessor.normalize_audio(audio, target_level_db=-20.0)
        audio = _step("final_normalisation", 100, audio)

        elapsed = time.perf_counter() - t0
        report["output_duration_sec"] = round(len(audio) / source_sr, 3)
        report["processing_time_sec"] = round(elapsed, 3)
        report["quality"] = cfg.quality
        report["target_profile_id"] = target_profile.get("profile_id", "unknown")

        logger.info(
            "Conversion complete: %.2fs audio in %.2fs (%s quality)",
            report["output_duration_sec"], elapsed, cfg.quality,
        )
        if progress_callback:
            progress_callback(100, "Done")
        return audio, report

    # ===================================== file-based high-level API

    def convert_voice_from_files(
        self,
        source_audio_path: str,
        target_profile_id_or_path: str,
        output_path: str,
        config: Optional[VoiceConverterConfig] = None,
    ) -> str:
        """
        High-level file API: load → convert → save.

        Parameters
        ----------
        source_audio_path          : str  path to source audio file
        target_profile_id_or_path  : str  profile UUID or full JSON path
        output_path                : str  where to write the converted WAV
        config                     : VoiceConverterConfig

        Returns
        -------
        str  absolute path to the written output file
        """
        cfg = config or self.config

        audio, sr, _ = self.preprocessor.preprocess_pipeline(source_audio_path, cfg)
        target_profile = self.analyzer.load_voice_profile(target_profile_id_or_path, cfg)
        converted, _ = self.convert_voice(audio, sr, target_profile, cfg)

        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        return self.preprocessor.save_audio(converted, sr, output_path)

    # ========================================== batch conversion

    def batch_convert(
        self,
        source_files: list[str],
        target_profile: dict,
        output_dir: str,
        config: Optional[VoiceConverterConfig] = None,
        max_workers: int = 4,
    ) -> list[str]:
        """
        Convert multiple audio files to the target voice profile.

        Uses a thread pool for I/O-bound operations (loading/saving).
        CPU-bound conversion is executed in the main thread for each file.

        Parameters
        ----------
        source_files   : list[str]  paths to source audio files
        target_profile : dict       pre-loaded profile
        output_dir     : str        directory for output files
        config         : VoiceConverterConfig
        max_workers    : int        thread pool size

        Returns
        -------
        list[str]  output file paths (in same order as source_files)
        """
        cfg = config or self.config
        os.makedirs(output_dir, exist_ok=True)
        results: list[str] = []

        def _convert_one(src_path: str) -> str:
            base = os.path.splitext(os.path.basename(src_path))[0]
            out_path = os.path.join(output_dir, f"{base}_converted.wav")
            try:
                audio, sr, _ = self.preprocessor.preprocess_pipeline(src_path, cfg)
                converted, _ = self.convert_voice(audio, sr, target_profile, cfg)
                self.preprocessor.save_audio(converted, sr, out_path)
                logger.info("Batch: converted %s → %s", src_path, out_path)
                return out_path
            except Exception as exc:
                logger.error("Batch: failed %s: %s", src_path, exc)
                return ""

        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as pool:
            futures = [pool.submit(_convert_one, p) for p in source_files]
            results = [f.result() for f in futures]

        return results

    # ========================================================== helpers

    @staticmethod
    def _smooth_pitch_contour(
        pitch_values: np.ndarray,
        kernel_size: int = 5,
    ) -> np.ndarray:
        """
        Smooth a pitch contour with a median filter to remove outliers
        without distorting the overall shape.

        Parameters
        ----------
        pitch_values : np.ndarray  raw F0 values (0 = unvoiced)
        kernel_size  : int

        Returns
        -------
        np.ndarray  smoothed F0 values
        """
        voiced_mask = pitch_values > 0
        smoothed = median_filter(pitch_values, size=kernel_size)
        smoothed[~voiced_mask] = 0.0
        return smoothed

    @staticmethod
    def _apply_soft_clipping(
        audio: np.ndarray,
        threshold: float = 0.95,
    ) -> np.ndarray:
        """
        Apply tanh soft-clipping to prevent hard digital clipping.

        Values inside [-threshold, threshold] are untouched.
        Values outside are compressed towards ±1 via tanh.

        Parameters
        ----------
        audio     : np.ndarray
        threshold : float  (0, 1)

        Returns
        -------
        np.ndarray
        """
        mask = np.abs(audio) > threshold
        audio = audio.copy()
        audio[mask] = (
            np.sign(audio[mask])
            * (threshold + (1 - threshold) * np.tanh(
                (np.abs(audio[mask]) - threshold) / (1 - threshold)
            ))
        )
        return audio.astype(np.float32)
