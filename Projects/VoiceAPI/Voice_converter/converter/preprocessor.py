"""
converter/preprocessor.py
==========================
Audio preprocessing pipeline for the Voice Converter Module.

Handles loading from multiple formats, resampling, mono conversion,
silence trimming, amplitude normalisation and validation before any
analysis or conversion is attempted.

Custom exception
----------------
AudioProcessingError  – raised for unrecoverable preprocessing failures.
"""

from __future__ import annotations

import io
import logging
import os
from typing import Union

import librosa
import numpy as np
import soundfile as sf

from .config import VoiceConverterConfig, DEFAULT_CONFIG

logger = logging.getLogger(__name__)


class AudioProcessingError(Exception):
    """Raised when audio cannot be loaded or preprocessed."""


class AudioPreprocessor:
    """
    Stateless helper that converts raw audio inputs into the canonical
    format expected by the analysis and conversion pipeline:

    * Sample rate : 22 050 Hz
    * Channels    : 1 (mono)
    * Dtype       : float32, range [-1.0, 1.0]
    """

    # ---------------------------------------------------------------- loading

    def load_audio(
        self,
        source: Union[str, bytes, io.IOBase],
        target_sr: int = 22_050,
    ) -> tuple[np.ndarray, int]:
        """
        Load audio from a file path, raw bytes, or a file-like object.

        Parameters
        ----------
        source : str | bytes | IO
            Path to an audio file (WAV/MP3/M4A/OGG/FLAC) **or** raw
            bytes of such a file **or** an already-open binary stream.
        target_sr : int
            Resample to this rate during load (librosa handles it).

        Returns
        -------
        audio : np.ndarray  float32, shape (n_samples,)
        sr    : int         actual sample-rate after resampling

        Raises
        ------
        AudioProcessingError
            If the file cannot be decoded.
        """
        try:
            if isinstance(source, (bytes, bytearray)):
                source = io.BytesIO(source)

            if isinstance(source, str):
                if not os.path.exists(source):
                    raise AudioProcessingError(f"File not found: {source}")
                audio, sr = librosa.load(source, sr=target_sr, mono=True)
            else:
                # file-like object (BytesIO, SpooledTemporaryFile, etc.)
                audio, sr = librosa.load(source, sr=target_sr, mono=True)

            logger.debug("Loaded audio: sr=%d, duration=%.2fs", sr, len(audio) / sr)
            return audio.astype(np.float32), sr

        except AudioProcessingError:
            raise
        except Exception as exc:
            raise AudioProcessingError(
                f"Failed to decode audio: {exc}"
            ) from exc

    # --------------------------------------------------------------- resample

    def resample_audio(
        self,
        audio: np.ndarray,
        orig_sr: int,
        target_sr: int = 22_050,
    ) -> np.ndarray:
        """
        Resample *audio* from *orig_sr* to *target_sr*.

        Uses ``librosa.resample`` with the ``kaiser_best`` filter for
        high perceptual quality.

        Parameters
        ----------
        audio     : np.ndarray  float32, 1-D
        orig_sr   : int
        target_sr : int

        Returns
        -------
        np.ndarray  float32, resampled
        """
        if orig_sr == target_sr:
            return audio

        resampled = librosa.resample(
            audio,
            orig_sr=orig_sr,
            target_sr=target_sr,
            res_type="kaiser_best",
        )
        logger.debug("Resampled %d Hz → %d Hz", orig_sr, target_sr)
        return resampled.astype(np.float32)

    # ------------------------------------------------------------------ mono

    def convert_to_mono(self, audio: np.ndarray) -> np.ndarray:
        """
        Convert a 2-D stereo array (channels × samples or samples ×
        channels) to 1-D mono by averaging channels.

        Parameters
        ----------
        audio : np.ndarray  shape (n_samples,) or (2, n_samples)

        Returns
        -------
        np.ndarray  shape (n_samples,)
        """
        if audio.ndim == 1:
            return audio
        if audio.ndim == 2:
            return audio.mean(axis=0).astype(np.float32)
        raise AudioProcessingError(
            f"Unexpected audio shape: {audio.shape} (expected 1-D or 2-D)"
        )

    # ----------------------------------------------------------- normalisation

    def normalize_audio(
        self,
        audio: np.ndarray,
        target_level_db: float = -20.0,
    ) -> np.ndarray:
        """
        RMS-normalise *audio* so its energy matches *target_level_db* dBFS.

        Parameters
        ----------
        audio            : np.ndarray  float32
        target_level_db  : float       e.g. -20.0 dBFS

        Returns
        -------
        np.ndarray  normalised, clipped to [-1, 1]
        """
        rms = np.sqrt(np.mean(audio ** 2))
        if rms < 1e-9:
            logger.warning("Near-silent audio; skipping normalisation")
            return audio

        target_rms = 10 ** (target_level_db / 20.0)
        gain = target_rms / rms
        normalised = audio * gain

        # Soft clip to prevent rare over-shoot
        normalised = np.clip(normalised, -1.0, 1.0)
        logger.debug(
            "Normalised: rms=%.4f → %.4f (gain=%.2f dB)",
            rms, target_rms, 20 * np.log10(gain),
        )
        return normalised.astype(np.float32)

    # ------------------------------------------------------------ trim silence

    def trim_silence(
        self,
        audio: np.ndarray,
        sr: int,
        top_db: float = 20.0,
    ) -> np.ndarray:
        """
        Remove leading and trailing silence using ``librosa.effects.trim``.

        Parameters
        ----------
        audio  : np.ndarray
        sr     : int         (unused here but kept for API symmetry)
        top_db : float       silence threshold in dB below peak

        Returns
        -------
        np.ndarray  trimmed audio
        """
        trimmed, _ = librosa.effects.trim(audio, top_db=top_db)
        removed = len(audio) - len(trimmed)
        logger.debug(
            "Trimmed %d samples (%.2f s) of silence",
            removed, removed / max(sr, 1),
        )
        return trimmed.astype(np.float32)

    # ---------------------------------------------------------------- validate

    def validate_audio(
        self,
        audio: np.ndarray,
        sr: int,
        config: VoiceConverterConfig = DEFAULT_CONFIG,
    ) -> dict:
        """
        Check whether *audio* satisfies the constraints in *config*.

        Parameters
        ----------
        audio  : np.ndarray
        sr     : int
        config : VoiceConverterConfig

        Returns
        -------
        dict with keys:
            valid    (bool)
            errors   (list[str])   – blocking problems
            warnings (list[str])   – non-blocking advisories
        """
        errors: list[str] = []
        warnings: list[str] = []

        duration = len(audio) / sr

        if duration < config.min_audio_duration_sec:
            errors.append(
                f"Audio too short: {duration:.2f}s < "
                f"min {config.min_audio_duration_sec}s"
            )
        if duration > config.max_audio_duration_sec:
            errors.append(
                f"Audio too long: {duration:.2f}s > "
                f"max {config.max_audio_duration_sec}s"
            )
        if sr != config.target_sample_rate:
            warnings.append(
                f"Sample rate {sr} Hz will be resampled to "
                f"{config.target_sample_rate} Hz"
            )

        rms = float(np.sqrt(np.mean(audio ** 2)))
        if rms < 1e-4:
            warnings.append("Audio appears nearly silent (RMS < 1e-4)")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "duration_sec": round(duration, 3),
            "sample_rate": sr,
            "rms": round(rms, 6),
        }

    # ------------------------------------------------------- full pipeline

    def preprocess_pipeline(
        self,
        audio_input: Union[str, bytes, io.IOBase],
        config: VoiceConverterConfig = DEFAULT_CONFIG,
    ) -> tuple[np.ndarray, int, dict]:
        """
        End-to-end preprocessing:

        1. Load (any format → float32 numpy)
        2. Validate (duration, level)
        3. Resample to ``config.target_sample_rate``
        4. Convert to mono
        5. Trim silence
        6. RMS-normalise to -20 dBFS

        Parameters
        ----------
        audio_input : str | bytes | IO
        config      : VoiceConverterConfig

        Returns
        -------
        audio    : np.ndarray  processed float32 audio
        sr       : int         sample rate (== config.target_sample_rate)
        metadata : dict        pipeline metadata (duration, sample_rate, rms …)

        Raises
        ------
        AudioProcessingError
            On load failure or validation errors.
        """
        logger.info("Starting preprocessing pipeline…")

        # 1. Load
        raw_audio, orig_sr = self.load_audio(
            audio_input,
            target_sr=None,  # type: ignore[arg-type]  load at native SR first
        )

        # librosa.load with sr=None keeps native SR; reload at native sr
        # Actually librosa.load with sr=None → returns (audio, orig_sr)
        # The call above already resamples if target_sr is set, so we
        # reload at native SR then resample explicitly for transparency.
        # Re-do load cleanly:
        raw_audio, orig_sr = librosa.load(
            audio_input if isinstance(audio_input, str)
            else (io.BytesIO(audio_input) if isinstance(audio_input, (bytes, bytearray)) else audio_input),
            sr=None,   # keep original
            mono=True,
        )
        raw_audio = raw_audio.astype(np.float32)

        # 2. Validate (before resampling, using original SR)
        validation = self.validate_audio(raw_audio, orig_sr, config)
        if not validation["valid"]:
            raise AudioProcessingError(
                "Audio validation failed: " + "; ".join(validation["errors"])
            )
        for w in validation.get("warnings", []):
            logger.warning("Validation warning: %s", w)

        # 3. Resample
        audio = self.resample_audio(raw_audio, orig_sr, config.target_sample_rate)
        sr = config.target_sample_rate

        # 4. Mono (librosa loads mono by default; guard anyway)
        audio = self.convert_to_mono(audio)

        # 5. Trim silence
        audio = self.trim_silence(audio, sr)

        # 6. Normalise
        audio = self.normalize_audio(audio, target_level_db=-20.0)

        metadata = {
            "original_sample_rate": orig_sr,
            "processed_sample_rate": sr,
            "duration_sec": round(len(audio) / sr, 3),
            "n_samples": len(audio),
            "rms": round(float(np.sqrt(np.mean(audio ** 2))), 6),
            "validation": validation,
        }
        logger.info(
            "Preprocessing complete: %.2f s @ %d Hz",
            metadata["duration_sec"], sr,
        )
        return audio, sr, metadata


    def save_audio(
        self,
        audio: np.ndarray,
        sr: int,
        output_path: str,
        subtype: str = "PCM_16",
    ) -> str:
        """
        Write *audio* to *output_path* as a WAV file.

        Parameters
        ----------
        audio       : np.ndarray  float32
        sr          : int
        output_path : str
        subtype     : str  soundfile subtype (default PCM_16)

        Returns
        -------
        str  absolute output path
        """
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        sf.write(output_path, audio, sr, subtype=subtype)
        logger.info("Saved audio: %s", output_path)
        return os.path.abspath(output_path)
