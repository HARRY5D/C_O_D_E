"""
converter/analyzer.py
======================
Voice characteristic extraction.

VoiceAnalyzer converts raw audio into a structured *voice profile*: a
JSON-serialisable dict of pitch, formant, spectral, energy, speaking-rate
and timbre statistics. Profiles are saved to disk and reloaded for
conversion.

Dependencies
------------
- parselmouth (Praat)  : pitch contour, formants, HNR, jitter, shimmer
- librosa              : spectral features, MFCCs, onset detection
- numpy / scipy        : statistics, filtering

Custom exceptions
-----------------
AnalysisError  – raised when feature extraction fails fatally.
"""

from __future__ import annotations

import json
import logging
import os
import uuid
from datetime import datetime, timezone
from typing import Optional

import librosa
import numpy as np
import parselmouth
from parselmouth.praat import call
from scipy.ndimage import median_filter

from .config import VoiceConverterConfig, DEFAULT_CONFIG

logger = logging.getLogger(__name__)


class AnalysisError(Exception):
    """Raised when voice-characteristic extraction fails."""


class VoiceAnalyzer:
    """
    Extracts voice characteristics from a preprocessed mono float32
    audio array and builds/persists JSON voice profiles.
    """

    # -------------------------------------------------------- pitch contour

    def extract_pitch_contour(
        self,
        audio: np.ndarray,
        sr: int,
        config: VoiceConverterConfig = DEFAULT_CONFIG,
    ) -> dict:
        """
        Extract fundamental frequency (F0) over time using Praat.

        Parameters
        ----------
        audio  : np.ndarray  float32, mono
        sr     : int
        config : VoiceConverterConfig

        Returns
        -------
        dict with keys:
            contour   (np.ndarray)  – F0 values (Hz), 0 where unvoiced
            times     (np.ndarray)  – corresponding time stamps (s)
            mean      (float)       – mean voiced F0
            std       (float)       – std dev of voiced F0
            min       (float)       – min voiced F0
            max       (float)       – max voiced F0
            voiced_ratio (float)    – fraction of voiced frames
        """
        try:
            snd = parselmouth.Sound(audio, sr)
            pitch_obj = snd.to_pitch(
                time_step=config.effective_hop_length() / sr,
                pitch_floor=config.pitch_range_hz[0],
                pitch_ceiling=config.pitch_range_hz[1],
            )
            times = pitch_obj.xs()
            contour = np.array([
                pitch_obj.get_value_at_time(t) or 0.0 for t in times
            ])

            voiced_mask = contour > 0
            voiced_f0 = contour[voiced_mask]

            if len(voiced_f0) == 0:
                logger.warning("No voiced frames detected in audio")
                return {
                    "contour": contour.tolist(),
                    "times": times.tolist(),
                    "mean": 0.0,
                    "std": 0.0,
                    "min": 0.0,
                    "max": 0.0,
                    "voiced_ratio": 0.0,
                }

            return {
                "contour": contour.tolist(),
                "times": times.tolist(),
                "mean": float(np.mean(voiced_f0)),
                "std": float(np.std(voiced_f0)),
                "min": float(np.min(voiced_f0)),
                "max": float(np.max(voiced_f0)),
                "voiced_ratio": float(voiced_mask.mean()),
            }
        except Exception as exc:
            raise AnalysisError(f"Pitch contour extraction failed: {exc}") from exc

    # ------------------------------------------------------------ formants

    def extract_formants(
        self,
        audio: np.ndarray,
        sr: int,
        n_formants: int = 5,
    ) -> dict:
        """
        Extract formant frequencies (F1–F5) using Praat LPC.

        Parameters
        ----------
        audio      : np.ndarray
        sr         : int
        n_formants : int  (max 5)

        Returns
        -------
        dict  { "F1": float, "F2": float, ..., "F5": float }
            Each value is the mean formant frequency (Hz) over voiced
            frames, or 0.0 if not detected.
        """
        try:
            snd = parselmouth.Sound(audio, sr)
            formant_obj = call(
                snd,
                "To Formant (burg)",
                0.0,          # time step (auto)
                n_formants,
                5500.0,       # max formant (Hz)  – female typical upper bound
                0.025,        # window length (s)
                50.0,         # pre-emphasis from (Hz)
            )
            n_frames = call(formant_obj, "Get number of frames")
            result: dict[str, float] = {}

            for fi in range(1, n_formants + 1):
                values = []
                for frame_idx in range(1, n_frames + 1):
                    t = call(formant_obj, "Get time from frame number", frame_idx)
                    v = call(formant_obj, "Get value at time", fi, t, "Hertz", "Linear")
                    if v and not np.isnan(v):
                        values.append(v)
                result[f"F{fi}"] = float(np.mean(values)) if values else 0.0

            logger.debug("Formants: %s", result)
            return result
        except Exception as exc:
            raise AnalysisError(f"Formant extraction failed: {exc}") from exc

    # --------------------------------------------------- spectral features

    def extract_spectral_features(
        self,
        audio: np.ndarray,
        sr: int,
    ) -> dict:
        """
        Compute STFT-based spectral statistics.

        Returns
        -------
        dict with keys:
            centroid_mean, centroid_std,
            rolloff_mean, rolloff_std,
            contrast_mean (per band),
            zcr_mean, zcr_std,
            mfcc_mean (13 coefficients),
            mfcc_std  (13 coefficients)
        """
        try:
            centroid = librosa.feature.spectral_centroid(y=audio, sr=sr)[0]
            rolloff = librosa.feature.spectral_rolloff(y=audio, sr=sr)[0]
            contrast = librosa.feature.spectral_contrast(y=audio, sr=sr)
            zcr = librosa.feature.zero_crossing_rate(y=audio)[0]
            mfcc = librosa.feature.mfcc(y=audio, sr=sr, n_mfcc=13)

            return {
                "centroid_mean": float(np.mean(centroid)),
                "centroid_std": float(np.std(centroid)),
                "rolloff_mean": float(np.mean(rolloff)),
                "rolloff_std": float(np.std(rolloff)),
                "contrast_mean": np.mean(contrast, axis=1).tolist(),
                "zcr_mean": float(np.mean(zcr)),
                "zcr_std": float(np.std(zcr)),
                "mfcc_mean": np.mean(mfcc, axis=1).tolist(),
                "mfcc_std": np.std(mfcc, axis=1).tolist(),
            }
        except Exception as exc:
            raise AnalysisError(f"Spectral feature extraction failed: {exc}") from exc

    # ------------------------------------------------------- energy contour

    def extract_energy_contour(
        self,
        audio: np.ndarray,
        sr: int,
    ) -> dict:
        """
        Compute frame-wise RMS energy statistics.

        Returns
        -------
        dict with keys:
            contour   (list[float])  – per-frame RMS
            mean      (float)
            std       (float)
            dynamic_range_db (float) – dB difference between loud/quiet
        """
        try:
            rms = librosa.feature.rms(y=audio)[0]
            rms_db = librosa.amplitude_to_db(rms, ref=np.max)
            dynamic_range = float(rms_db.max() - rms_db.min())

            return {
                "contour": rms.tolist(),
                "mean": float(np.mean(rms)),
                "std": float(np.std(rms)),
                "dynamic_range_db": dynamic_range,
            }
        except Exception as exc:
            raise AnalysisError(f"Energy contour extraction failed: {exc}") from exc

    # ----------------------------------------------------- speaking rate

    def extract_speaking_rate(
        self,
        audio: np.ndarray,
        sr: int,
    ) -> dict:
        """
        Estimate speaking rate via onset detection.

        Returns
        -------
        dict with keys:
            syllables_per_sec (float)
            n_onsets          (int)
            pause_ratio       (float) – fraction of silent frames
        """
        try:
            onsets = librosa.onset.onset_detect(y=audio, sr=sr, units="time")
            duration = len(audio) / sr
            syllables_per_sec = len(onsets) / max(duration, 1e-6)

            # Simple silence detection via energy threshold
            rms = librosa.feature.rms(y=audio)[0]
            silence_threshold = np.percentile(rms, 15)
            pause_ratio = float(np.mean(rms < silence_threshold))

            return {
                "syllables_per_sec": round(syllables_per_sec, 3),
                "n_onsets": int(len(onsets)),
                "pause_ratio": round(pause_ratio, 4),
            }
        except Exception as exc:
            raise AnalysisError(f"Speaking rate extraction failed: {exc}") from exc

    # ------------------------------------------------------------ timbre

    def extract_voice_timbre(
        self,
        audio: np.ndarray,
        sr: int,
    ) -> dict:
        """
        Compute timbre quality metrics using Praat.

        Returns
        -------
        dict with keys:
            hnr_mean_db  (float)  – harmonics-to-noise ratio (dB)
            jitter       (float)  – local jitter (%)
            shimmer      (float)  – local shimmer (dB)
            spectral_flux_mean (float)
        """
        try:
            snd = parselmouth.Sound(audio, sr)

            # HNR
            hnr_obj = call(snd, "To Harmonicity (cc)", 0.01, 75, 0.1, 1.0)
            hnr_mean = call(hnr_obj, "Get mean", 0, 0)
            hnr_mean = float(hnr_mean) if hnr_mean and not np.isnan(hnr_mean) else 0.0

            # Jitter & shimmer via PointProcess
            pp = call(snd, "To PointProcess (periodic, cc)", 75, 500)
            jitter = call(pp, "Get jitter (local)", 0, 0, 0.0001, 0.02, 1.3)
            shimmer = call([snd, pp], "Get shimmer (local_dB)", 0, 0, 0.0001, 0.02, 1.3, 1.6)
            jitter = float(jitter) if jitter and not np.isnan(jitter) else 0.0
            shimmer = float(shimmer) if shimmer and not np.isnan(shimmer) else 0.0

            # Spectral flux
            stft = np.abs(librosa.stft(audio))
            flux = np.mean(np.diff(stft, axis=1) ** 2)

            return {
                "hnr_mean_db": round(hnr_mean, 4),
                "jitter": round(jitter, 6),
                "shimmer": round(shimmer, 6),
                "spectral_flux_mean": round(float(flux), 6),
            }
        except Exception as exc:
            logger.warning("Timbre extraction partial failure: %s", exc)
            return {
                "hnr_mean_db": 0.0,
                "jitter": 0.0,
                "shimmer": 0.0,
                "spectral_flux_mean": 0.0,
            }

    # ------------------------------------------------- create profile

    def create_voice_profile(
        self,
        audio: np.ndarray,
        sr: int,
        config: VoiceConverterConfig,
        profile_name: str,
        save: bool = True,
    ) -> dict:
        """
        Build a complete voice profile from preprocessed audio and
        optionally persist it as JSON.

        Parameters
        ----------
        audio        : np.ndarray  preprocessed, float32, mono
        sr           : int
        config       : VoiceConverterConfig
        profile_name : str   human-readable label
        save         : bool  write profile JSON to disk

        Returns
        -------
        dict  full voice profile
        """
        logger.info("Creating voice profile: %s", profile_name)

        profile_id = str(uuid.uuid4())
        duration = len(audio) / sr

        pitch = self.extract_pitch_contour(audio, sr, config)
        formants = self.extract_formants(audio, sr)
        spectral = self.extract_spectral_features(audio, sr)
        energy = self.extract_energy_contour(audio, sr)
        speaking_rate = self.extract_speaking_rate(audio, sr)
        timbre = self.extract_voice_timbre(audio, sr)

        profile: dict = {
            "profile_id": profile_id,
            "profile_name": profile_name,
            "timestamp": datetime.now(tz=timezone.utc).isoformat(),
            "audio_duration": round(duration, 3),
            "sample_rate": sr,
            "pitch": {
                "mean": round(pitch["mean"], 3),
                "std": round(pitch["std"], 3),
                "min": round(pitch["min"], 3),
                "max": round(pitch["max"], 3),
                "voiced_ratio": round(pitch["voiced_ratio"], 4),
                # Full contour NOT saved to JSON (too large) – kept in memory
            },
            "pitch_contour": pitch["contour"],   # list[float] in-memory only
            "formants": formants,
            "spectral": spectral,
            "energy": {
                "mean": round(energy["mean"], 6),
                "std": round(energy["std"], 6),
                "dynamic_range_db": round(energy["dynamic_range_db"], 3),
                "contour": energy["contour"],  # kept in-memory
            },
            "speaking_rate": speaking_rate,
            "timbre": timbre,
        }

        if save:
            self._save_profile(profile, config)

        logger.info(
            "Profile created: id=%s, pitch=%.1f Hz, duration=%.2f s",
            profile_id, pitch["mean"], duration,
        )
        return profile

    def _save_profile(self, profile: dict, config: VoiceConverterConfig) -> str:
        """Persist *profile* to ``config.voice_profiles_dir``."""
        config.ensure_dirs()
        # Strip large in-memory arrays before serialising
        saveable = {k: v for k, v in profile.items()
                    if k not in ("pitch_contour",)}
        saveable["energy"] = {
            k: v for k, v in profile["energy"].items()
            if k != "contour"
        }

        path = os.path.join(
            config.voice_profiles_dir,
            f"profile_{profile['profile_id']}.json",
        )
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(saveable, fh, indent=2, ensure_ascii=False)
        logger.info("Profile saved: %s", path)
        return path

    # -------------------------------------------------- load profile

    def load_voice_profile(
        self,
        profile_id_or_path: str,
        config: VoiceConverterConfig = DEFAULT_CONFIG,
    ) -> dict:
        """
        Load a saved voice profile from disk.

        Parameters
        ----------
        profile_id_or_path : str
            Either a UUID (looked up in ``config.voice_profiles_dir``) or
            a full file path to the JSON.
        config             : VoiceConverterConfig

        Returns
        -------
        dict  profile (same structure as returned by create_voice_profile)

        Raises
        ------
        AnalysisError  if file not found or JSON is malformed.
        """
        if os.path.isfile(profile_id_or_path):
            path = profile_id_or_path
        else:
            path = os.path.join(
                config.voice_profiles_dir,
                f"profile_{profile_id_or_path}.json",
            )

        if not os.path.exists(path):
            raise AnalysisError(f"Voice profile not found: {path}")

        try:
            with open(path, encoding="utf-8") as fh:
                profile = json.load(fh)
        except json.JSONDecodeError as exc:
            raise AnalysisError(f"Corrupt profile JSON: {path}: {exc}") from exc

        # Minimal structure validation
        required = {"profile_id", "profile_name", "pitch", "formants"}
        missing = required - set(profile.keys())
        if missing:
            raise AnalysisError(
                f"Profile {path} missing required keys: {missing}"
            )

        logger.info("Loaded voice profile: %s (%s)", profile["profile_name"], profile["profile_id"])
        return profile

    # -------------------------------------------- list profiles

    def list_profiles(
        self,
        config: VoiceConverterConfig = DEFAULT_CONFIG,
    ) -> list[dict]:
        """
        Return summary info for all saved profiles.

        Returns
        -------
        list[dict]  each dict has: id, name, created_at, duration, pitch_mean
        """
        profiles_dir = config.voice_profiles_dir
        if not os.path.isdir(profiles_dir):
            return []

        summaries = []
        for fname in os.listdir(profiles_dir):
            if not fname.endswith(".json"):
                continue
            try:
                path = os.path.join(profiles_dir, fname)
                with open(path, encoding="utf-8") as fh:
                    p = json.load(fh)
                summaries.append({
                    "id": p.get("profile_id", ""),
                    "name": p.get("profile_name", ""),
                    "created_at": p.get("timestamp", ""),
                    "duration": p.get("audio_duration", 0.0),
                    "pitch_mean": p.get("pitch", {}).get("mean", 0.0),
                })
            except Exception as exc:
                logger.warning("Skipping corrupt profile %s: %s", fname, exc)

        return sorted(summaries, key=lambda x: x["created_at"], reverse=True)
