"""
converter/__init__.py
======================
Public API for the voice-converter module.

Typical usage::

    from converter import (
        AudioPreprocessor,
        VoiceAnalyzer,
        VoiceConverter,
        VoiceConverterConfig,
        DEFAULT_CONFIG,
    )

    preprocessor = AudioPreprocessor()
    audio, sr, meta = preprocessor.preprocess_pipeline("my_voice.wav", DEFAULT_CONFIG)

    analyzer = VoiceAnalyzer()
    profile = analyzer.create_voice_profile(audio, sr, DEFAULT_CONFIG, "MyVoice")

    converter = VoiceConverter(DEFAULT_CONFIG)
    converted, report = converter.convert_voice(tts_audio, 22050, profile)
"""

from .config import VoiceConverterConfig, DEFAULT_CONFIG
from .preprocessor import AudioPreprocessor, AudioProcessingError
from .analyzer import VoiceAnalyzer, AnalysisError
from .converter import VoiceConverter

__all__ = [
    "VoiceConverterConfig",
    "DEFAULT_CONFIG",
    "AudioPreprocessor",
    "AudioProcessingError",
    "VoiceAnalyzer",
    "AnalysisError",
    "VoiceConverter",
]
