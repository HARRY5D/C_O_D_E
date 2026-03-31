"""
converter/config.py
====================
Central configuration for the Voice Converter Module.

All tuneable parameters live here so callers never hard-code magic
numbers.  Pass a custom VoiceConverterConfig instance to any
converter/analyzer/preprocessor method to override defaults.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Literal, Tuple


@dataclass
class VoiceConverterConfig:
    """
    Immutable-friendly dataclass holding all runtime parameters for
    the voice-conversion pipeline.

    Attributes
    ----------
    target_sample_rate : int
        All audio is resampled to this rate before processing (Hz).
        VoiceAPI models output 22 050 Hz, so the default matches.
    target_channels : int
        1 = mono (required by all downstream algorithms).
    target_bit_depth : int
        PCM bit depth for exported WAV files.
    pitch_range_hz : tuple[float, float]
        Acceptable voiced-pitch range; anything outside is treated as
        unvoiced during analysis.
    hop_length : int
        STFT hop size in samples (lower = finer time resolution, slower).
    win_length : int
        STFT window size in samples.
    n_fft : int
        FFT size (must be >= win_length).
    pitch_shift_method : "librosa" | "parselmouth"
        Backend used for pitch shifting.
        - "librosa"      : phase-vocoder (fast, slight artefacts).
        - "parselmouth"  : Praat PSOLA (higher quality, ~2x slower).
    formant_shift_enabled : bool
        When True, formant envelopes are shifted to match the target profile.
    energy_normalization : bool
        When True, per-frame RMS energy is matched to the target profile.
    quality : "fast" | "balanced" | "high"
        Presets that adjust n_fft / hop_length and pitch-estimation
        algorithm.  Higher quality means more CPU time.
    voice_profiles_dir : str
        Directory where JSON voice profiles are saved/loaded.
    temp_audio_dir : str
        Directory for temporary intermediate audio files.
    min_audio_duration_sec : float
        Reject audio shorter than this during validation.
    max_audio_duration_sec : float
        Reject audio longer than this during validation.
    max_file_size_mb : float
        Reject uploaded audio files larger than this (MB).
    """

    # ------------------------------------------------------------------ audio
    target_sample_rate: int = 22_050
    target_channels: int = 1
    target_bit_depth: int = 16

    # --------------------------------------------------------- analysis params
    pitch_range_hz: Tuple[float, float] = (75.0, 600.0)
    hop_length: int = 256
    win_length: int = 1024
    n_fft: int = 2048

    # ------------------------------------------------------- conversion params
    pitch_shift_method: Literal["librosa", "parselmouth"] = "librosa"
    formant_shift_enabled: bool = True
    energy_normalization: bool = True

    # ----------------------------------------------------------------- quality
    quality: Literal["fast", "balanced", "high"] = "balanced"

    # ------------------------------------------------------------------ paths
    voice_profiles_dir: str = field(
        default_factory=lambda: os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "models", "voice_profiles"
        )
    )
    temp_audio_dir: str = field(
        default_factory=lambda: os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "temp"
        )
    )

    # --------------------------------------------------------------- limits
    min_audio_duration_sec: float = 3.0
    max_audio_duration_sec: float = 30.0
    max_file_size_mb: float = 10.0

    # ------------------------------------------------------ derived settings
    def get_quality_settings(self) -> dict:
        """
        Return a dict of algorithm parameters tuned for the chosen
        quality preset.

        Returns
        -------
        dict
            Keys: n_fft, hop_length, pitch_estimation_method
        """
        presets: dict[str, dict] = {
            "fast": {
                "n_fft": 1024,
                "hop_length": 512,
                "pitch_estimation_method": "pyin",
            },
            "balanced": {
                "n_fft": 2048,
                "hop_length": 256,
                "pitch_estimation_method": "pyin",
            },
            "high": {
                "n_fft": 4096,
                "hop_length": 128,
                "pitch_estimation_method": "pyin",   # CREPE optional: heavy dep
            },
        }
        return presets[self.quality]

    def effective_n_fft(self) -> int:
        """Return n_fft adjusted for the current quality preset."""
        return self.get_quality_settings()["n_fft"]

    def effective_hop_length(self) -> int:
        """Return hop_length adjusted for the current quality preset."""
        return self.get_quality_settings()["hop_length"]

    def ensure_dirs(self) -> None:
        """Create voice_profiles_dir and temp_audio_dir if missing."""
        os.makedirs(self.voice_profiles_dir, exist_ok=True)
        os.makedirs(self.temp_audio_dir, exist_ok=True)


# Convenience singleton — most callers import just this.
DEFAULT_CONFIG = VoiceConverterConfig()
