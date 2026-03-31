"""
generate_samples.py
===================
Generates synthetic voice-like WAV files for testing the Voice Converter.

No extra dependencies beyond those already in requirements.txt.
Uses numpy + scipy to synthesise voiced speech with realistic harmonic
structure and formant resonances.

Run from the Voice_converter directory:
    python tests/generate_samples.py
"""

from __future__ import annotations

import os
import wave

import numpy as np
from scipy.signal import butter, lfilter, sosfilt
from scipy.io import wavfile

SAMPLE_RATE = 22050
OUT_DIR = os.path.join(os.path.dirname(__file__), "sample_audios")
os.makedirs(OUT_DIR, exist_ok=True)


# ─── Low-level DSP helpers ─────────────────────────────────────────────────

def _glottal_pulse_train(f0: float, duration: float, sr: int) -> np.ndarray:
    """Generate a periodic pulse train (glottal source) at frequency f0."""
    n_samples = int(duration * sr)
    t = np.arange(n_samples) / sr
    period = 1.0 / f0
    # Sawtooth-shaped pulses (standard glottal approximation)
    signal = np.zeros(n_samples)
    pulse_pos = np.arange(0, duration, period)
    for p in pulse_pos:
        idx = int(p * sr)
        if idx < n_samples:
            # decaying exponential per period
            end = min(idx + int(period * sr), n_samples)
            pulse_len = end - idx
            signal[idx:end] += np.exp(-np.linspace(0, 6, pulse_len))
    return signal


def _bandpass(signal: np.ndarray, lo: float, hi: float, sr: int,
              order: int = 4) -> np.ndarray:
    """Apply a Butterworth bandpass filter."""
    nyq = sr / 2.0
    sos = butter(order, [lo / nyq, hi / nyq], btype="band", output="sos")
    return sosfilt(sos, signal)


def _formant_filter(signal: np.ndarray, formant_freqs: list[float],
                    bw: float, sr: int) -> np.ndarray:
    """Cascade resonance filters to model the vocal tract."""
    out = signal.copy()
    for f in formant_freqs:
        out = _bandpass(out, max(50, f - bw / 2), min(sr / 2 - 1, f + bw / 2), sr)
    # add the filtered versions back to the original (additive)
    return signal * 0.3 + out * 0.7


def _normalise(signal: np.ndarray, peak: float = 0.7) -> np.ndarray:
    mx = np.max(np.abs(signal))
    if mx > 0:
        signal = signal / mx * peak
    return signal


def _add_breath_noise(signal: np.ndarray, level: float = 0.02) -> np.ndarray:
    """Add a small amount of breath noise for realism."""
    noise = np.random.randn(len(signal)) * level
    return signal + noise


def synthesise_voice(
    f0: float,
    duration: float,
    formants: list[float],
    formant_bw: float = 180.0,
    sr: int = SAMPLE_RATE,
    tremolo_hz: float = 5.0,
    vibrato_cents: float = 20.0,
) -> np.ndarray:
    """
    Synthesise a voiced speech segment.
    
    Parameters
    ----------
    f0        : Fundamental frequency in Hz (pitch)
    duration  : Length in seconds
    formants  : List of formant centre frequencies [F1, F2, F3, ...]
    formant_bw: Formant bandwidth in Hz
    sr        : Sample rate
    tremolo_hz: Amplitude modulation frequency (naturalness)
    vibrato_cents: Pitch vibrato depth in cents
    """
    n = int(duration * sr)
    t = np.arange(n) / sr

    # Slight pitch vibrato
    vibrato = 1.0 + (vibrato_cents / 1200.0) * np.sin(2 * np.pi * 2.5 * t)
    
    # Harmonic stack (voiced excitation)
    source = np.zeros(n)
    max_harmonic = int(sr / (2 * f0))
    for k in range(1, min(max_harmonic, 30)):
        amp = 1.0 / (k ** 1.2)   # roll-off ~6 dB/octave
        phase = np.random.uniform(0, 2 * np.pi)
        source += amp * np.sin(2 * np.pi * k * f0 * vibrato * t + phase)

    # Vocal tract resonances
    signal = _formant_filter(source, formants, formant_bw, sr)

    # Amplitude envelope (natural attack/release)
    env = np.ones(n)
    attack = int(0.05 * sr)
    release = int(0.08 * sr)
    if attack > 0:
        env[:attack] = np.linspace(0, 1, attack)
    if release > 0 and release <= n:
        env[-release:] = np.linspace(1, 0, release)

    signal *= env

    # Tremolo (amplitude modulation at ~5 Hz)
    tremolo = 1.0 + 0.08 * np.sin(2 * np.pi * tremolo_hz * t)
    signal *= tremolo

    # Breath noise
    signal = _add_breath_noise(signal, level=0.015)

    return _normalise(signal)


def save_wav(filename: str, signal: np.ndarray, sr: int = SAMPLE_RATE) -> str:
    """Save float32 signal to 16-bit WAV."""
    path = os.path.join(OUT_DIR, filename)
    pcm = (signal * 32767).astype(np.int16)
    wavfile.write(path, sr, pcm)
    print(f"  ✓ Saved: {path}  ({len(signal)/sr:.1f}s)")
    return path


# ─── Voice profiles ────────────────────────────────────────────────────────

def _generate_voice_a(duration: float) -> np.ndarray:
    """
    Voice A – Female-like (higher pitch ~200 Hz, brighter formants).
    Use this as the REFERENCE voice profile.
    """
    return synthesise_voice(
        f0=200.0,
        duration=duration,
        formants=[800, 1800, 2700, 3500],   # female-ish F1-F4
        formant_bw=150.0,
        tremolo_hz=4.5,
        vibrato_cents=18.0,
    )


def _generate_voice_b(duration: float) -> np.ndarray:
    """
    Voice B – Male-like (lower pitch ~120 Hz, deeper formants).
    Use this as the SOURCE that gets converted to Voice A.
    """
    return synthesise_voice(
        f0=120.0,
        duration=duration,
        formants=[550, 1100, 2500, 3200],   # male-ish F1-F4
        formant_bw=200.0,
        tremolo_hz=5.5,
        vibrato_cents=25.0,
    )


def _generate_child_voice(duration: float) -> np.ndarray:
    """Voice C – Child-like (high pitch ~300 Hz)."""
    return synthesise_voice(
        f0=300.0,
        duration=duration,
        formants=[900, 2000, 3000, 3800],
        formant_bw=120.0,
        tremolo_hz=6.0,
        vibrato_cents=12.0,
    )


# ─── Sentence-like segments (with pauses for more realistic prosody) ───────

def _sentence(voice_fn, word_durations: list[float],
              pause: float = 0.12) -> np.ndarray:
    """Build a 'sentence' from word-length voiced segments + silence pauses."""
    silence = np.zeros(int(pause * SAMPLE_RATE))
    chunks = []
    for dur in word_durations:
        chunks.append(voice_fn(dur))
        chunks.append(silence)
    return np.concatenate(chunks)


# ─── Main generator ─────────────────────────────────────────────────────────

def main() -> None:
    np.random.seed(42)

    print("\n🎙  Generating synthetic voice samples…\n")

    # 1. Reference voice (≥5 s recommended for profile creation)
    print("1. reference_voice_A.wav  — Female-like voice (use as voice profile)")
    sample = _sentence(_generate_voice_a,
                       [0.35, 0.28, 0.42, 0.31, 0.38,   # "sentence 1"
                        0.27, 0.45, 0.30, 0.36, 0.29,   # "sentence 2"
                        0.40, 0.25, 0.33, 0.38, 0.28],  # "sentence 3"
                       pause=0.10)
    save_wav("reference_voice_A.wav", sample)

    # 2. Source audio (male-like, shorter – the one to be converted)
    print("\n2. source_audio_B.wav     — Male-like voice (to be converted)")
    sample = _sentence(_generate_voice_b,
                       [0.38, 0.30, 0.44, 0.28, 0.36,
                        0.32, 0.41, 0.27, 0.35, 0.31],
                       pause=0.12)
    save_wav("source_audio_B.wav", sample)

    # 3. Child voice reference
    print("\n3. reference_voice_C.wav  — Child-like voice (extra profile)")
    sample = _sentence(_generate_child_voice,
                       [0.25, 0.20, 0.30, 0.22, 0.28,
                        0.18, 0.32, 0.24, 0.27, 0.21,
                        0.19, 0.26, 0.31, 0.23, 0.20],
                       pause=0.08)
    save_wav("reference_voice_C.wav", sample)

    # 4. Short male snippet for "convert-with-new-voice" endpoint
    print("\n4. short_source_5s.wav    — Short source clip (5 s)")
    sample = _sentence(_generate_voice_b,
                       [0.40, 0.35, 0.50, 0.38, 0.42],
                       pause=0.15)
    save_wav("short_source_5s.wav", sample)

    # 5. Identical content, two voices – useful for direct A/B comparison
    print("\n5. same_content_voice_A.wav  — Same prosody, Voice A")
    words = [0.34, 0.27, 0.39, 0.30, 0.35, 0.28, 0.41]
    save_wav("same_content_voice_A.wav",
             _sentence(_generate_voice_a, words))

    print("\n6. same_content_voice_B.wav  — Same prosody, Voice B")
    save_wav("same_content_voice_B.wav",
             _sentence(_generate_voice_b, words))

    print("\n✅  All samples saved to:", OUT_DIR)
    print("""
─────────────────────────────────────────────────────────────────
Quick test guide
─────────────────────────────────────────────────────────────────
Reference audio (for creating a voice profile):
  → reference_voice_A.wav   (female-like, ~5 s)
  → reference_voice_C.wav   (child-like, ~5 s)

Source audio (audio files to convert):
  → source_audio_B.wav      (male-like voice, ~4 s)
  → short_source_5s.wav     (male-like, ~5 s)

A/B comparison pair (same prosody, different voice):
  → same_content_voice_A.wav
  → same_content_voice_B.wav

Steps:
  1. Start converter:  uvicorn api.main:app --port 8002 (from Voice_converter/)
  2. Upload reference_voice_A.wav  →  POST /api/create-voice-profile
  3. Convert source_audio_B.wav    →  POST /api/convert  (with the profile id)
─────────────────────────────────────────────────────────────────
""")


if __name__ == "__main__":
    main()
