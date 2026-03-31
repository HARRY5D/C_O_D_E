"""
api/main.py
============
FastAPI server for the Voice Converter Module.

Endpoints
---------
POST   /api/create-voice-profile        – Upload reference audio → build voice profile
GET    /api/voice-profiles              – List all saved profiles
DELETE /api/voice-profiles/{profile_id} – Delete a profile
POST   /api/convert                     – Convert source audio with saved profile
POST   /api/convert-with-new-voice      – Convert source audio using uploaded reference
GET    /api/health                      – Health check

Usage
-----
    uvicorn api.main:app --reload --port 8002
"""

from __future__ import annotations

import io
import logging
import os
import sys
import time
import uuid
from contextlib import asynccontextmanager
from typing import Literal, Optional

import aiofiles
import numpy as np
import soundfile as sf
from dotenv import load_dotenv
from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

# --- add Voice_converter root to path so `converter` package is importable ---
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from converter import (
    DEFAULT_CONFIG,
    AnalysisError,
    AudioProcessingError,
    AudioPreprocessor,
    VoiceAnalyzer,
    VoiceConverter,
    VoiceConverterConfig,
)

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(name)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger("voice_converter.api")

# ---------------------------------------------------------------------------
# Configuration from environment
# ---------------------------------------------------------------------------
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")
HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8002"))
MAX_FILE_SIZE_MB = float(os.getenv("MAX_FILE_SIZE_MB", "10"))

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
TEMP_DIR = os.path.join(BASE_DIR, "temp")

# ---------------------------------------------------------------------------
# Module-level singletons (re-used across requests)
# ---------------------------------------------------------------------------
preprocessor = AudioPreprocessor()
analyzer = VoiceAnalyzer()

# ---------------------------------------------------------------------------
# Lifespan
# ---------------------------------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("=" * 60)
    logger.info("🎙️  Voice Converter API Starting…")
    logger.info("=" * 60)
    os.makedirs(TEMP_DIR, exist_ok=True)
    DEFAULT_CONFIG.ensure_dirs()
    logger.info("Profiles dir : %s", DEFAULT_CONFIG.voice_profiles_dir)
    logger.info("Temp dir     : %s", TEMP_DIR)
    logger.info("Server       : http://%s:%d", HOST, PORT)
    logger.info("API Docs     : http://%s:%d/docs", HOST, PORT)
    logger.info("=" * 60)
    yield
    logger.info("Voice Converter API shutting down")


# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------
app = FastAPI(
    title="Voice Converter API",
    description=(
        "Standalone voice conversion microservice. "
        "Convert any TTS output to sound like a custom voice profile."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve the frontend SPA from /
frontend_dir = os.path.join(BASE_DIR, "frontend")
if os.path.isdir(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


# ---------------------------------------------------------------------------
# Pydantic response models
# ---------------------------------------------------------------------------

class ProfileSummary(BaseModel):
    id: str
    name: str
    created_at: str
    duration: float
    pitch_mean: float


class ProfileListResponse(BaseModel):
    profiles: list[ProfileSummary]


class CreateProfileResponse(BaseModel):
    profile_id: str
    profile_name: str
    status: str
    characteristics: dict


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    profiles_dir: str
    n_profiles: int


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

async def _read_upload(upload: UploadFile, max_mb: float = MAX_FILE_SIZE_MB) -> bytes:
    """Read an UploadFile, enforcing max size."""
    data = await upload.read()
    if len(data) > max_mb * 1024 * 1024:
        raise HTTPException(
            status_code=413,
            detail=f"File exceeds maximum size of {max_mb} MB",
        )
    return data


def _audio_to_wav_bytes(audio: np.ndarray, sr: int) -> bytes:
    """Encode a numpy audio array to WAV bytes (16-bit PCM)."""
    buf = io.BytesIO()
    sf.write(buf, audio, sr, format="WAV", subtype="PCM_16")
    buf.seek(0)
    return buf.read()


def _build_config_from_quality(quality: str) -> VoiceConverterConfig:
    from dataclasses import replace
    q = quality if quality in ("fast", "balanced", "high") else "balanced"
    return VoiceConverterConfig(quality=q)  # type: ignore[call-arg]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/", include_in_schema=False)
async def root():
    """Serve frontend index.html if present."""
    index = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index):
        return FileResponse(index)
    return JSONResponse({"message": "Voice Converter API – visit /docs"})


@app.get("/api/health", response_model=HealthResponse)
async def health():
    """Return server health and profile count."""
    from datetime import datetime, timezone
    profiles = analyzer.list_profiles(DEFAULT_CONFIG)
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(tz=timezone.utc).isoformat(),
        profiles_dir=DEFAULT_CONFIG.voice_profiles_dir,
        n_profiles=len(profiles),
    )


# ------------------------------------------------------------------
# Profile management
# ------------------------------------------------------------------

@app.post("/api/create-voice-profile", response_model=CreateProfileResponse)
async def create_voice_profile(
    reference_audio: UploadFile = File(..., description="WAV/MP3/OGG reference recording (≥3 s)"),
    profile_name: str = Form(..., min_length=1, max_length=80),
):
    """
    Upload a reference audio clip and extract a voice profile.

    The audio should be at least 3 seconds of clean speech.
    """
    raw = await _read_upload(reference_audio)

    try:
        audio, sr, meta = preprocessor.preprocess_pipeline(raw, DEFAULT_CONFIG)
    except AudioProcessingError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    try:
        profile = analyzer.create_voice_profile(
            audio, sr, DEFAULT_CONFIG, profile_name, save=True
        )
    except AnalysisError as exc:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {exc}")

    return CreateProfileResponse(
        profile_id=profile["profile_id"],
        profile_name=profile["profile_name"],
        status="success",
        characteristics={
            "pitch_mean_hz": profile["pitch"]["mean"],
            "duration_sec": profile["audio_duration"],
            "sample_rate": profile["sample_rate"],
            "voiced_ratio": profile["pitch"]["voiced_ratio"],
            "formant_f1_hz": profile["formants"].get("F1", 0),
            "formant_f2_hz": profile["formants"].get("F2", 0),
            "speaking_rate_sps": profile["speaking_rate"].get("syllables_per_sec", 0),
            "hnr_db": profile["timbre"].get("hnr_mean_db", 0),
        },
    )


@app.get("/api/voice-profiles", response_model=ProfileListResponse)
async def list_voice_profiles():
    """Return all saved voice profiles ordered by creation date (newest first)."""
    profiles = analyzer.list_profiles(DEFAULT_CONFIG)
    return ProfileListResponse(
        profiles=[ProfileSummary(**p) for p in profiles]
    )


@app.delete("/api/voice-profiles/{profile_id}")
async def delete_voice_profile(profile_id: str):
    """Delete a saved voice profile by its UUID."""
    path = os.path.join(
        DEFAULT_CONFIG.voice_profiles_dir, f"profile_{profile_id}.json"
    )
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Profile not found")
    os.remove(path)
    logger.info("Deleted profile: %s", profile_id)
    return {"status": "deleted", "profile_id": profile_id}


# ------------------------------------------------------------------
# Conversion
# ------------------------------------------------------------------

@app.post("/api/convert")
async def convert_audio(
    source_audio: UploadFile = File(..., description="Source audio (TTS output or recording)"),
    target_profile_id: str = Form(..., description="UUID of the target voice profile"),
    quality: str = Form("balanced", description="fast | balanced | high"),
):
    """
    Convert *source_audio* to sound like the voice in *target_profile_id*.

    Returns a WAV audio/wav response with conversion metadata headers.
    """
    raw = await _read_upload(source_audio)
    cfg = _build_config_from_quality(quality)

    try:
        audio, sr, _ = preprocessor.preprocess_pipeline(raw, cfg)
    except AudioProcessingError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    try:
        target_profile = analyzer.load_voice_profile(target_profile_id, DEFAULT_CONFIG)
    except AnalysisError as exc:
        raise HTTPException(status_code=404, detail=str(exc))

    converter = VoiceConverter(cfg)
    t0 = time.perf_counter()
    try:
        converted, report = converter.convert_voice(audio, sr, target_profile, cfg)
    except Exception as exc:
        logger.exception("Conversion failed")
        raise HTTPException(status_code=500, detail=f"Conversion error: {exc}")

    elapsed = time.perf_counter() - t0
    wav_bytes = _audio_to_wav_bytes(converted, sr)

    return StreamingResponse(
        io.BytesIO(wav_bytes),
        media_type="audio/wav",
        headers={
            "Content-Disposition": "attachment; filename=converted.wav",
            "X-Conversion-Method": "voice_converter_v1",
            "X-Source-Duration": str(report.get("source_duration_sec", "")),
            "X-Processing-Time": f"{elapsed:.3f}s",
            "X-Quality": quality,
            "X-Target-Profile": target_profile_id,
            "X-Target-Pitch": f"{target_profile.get('pitch', {}).get('mean', 0):.1f}Hz",
        },
    )


@app.post("/api/convert-with-new-voice")
async def convert_with_new_voice(
    source_audio: UploadFile = File(..., description="Source audio to convert"),
    target_reference_audio: UploadFile = File(..., description="Target voice reference (≥3 s)"),
    quality: str = Form("balanced"),
):
    """
    Convert *source_audio* to match the voice in *target_reference_audio*
    without saving a persistent profile.

    Useful for one-shot conversions.
    """
    src_raw = await _read_upload(source_audio)
    ref_raw = await _read_upload(target_reference_audio)
    cfg = _build_config_from_quality(quality)

    try:
        src_audio, src_sr, _ = preprocessor.preprocess_pipeline(src_raw, cfg)
        ref_audio, ref_sr, _ = preprocessor.preprocess_pipeline(ref_raw, cfg)
    except AudioProcessingError as exc:
        raise HTTPException(status_code=422, detail=str(exc))

    try:
        temp_profile = analyzer.create_voice_profile(
            ref_audio, ref_sr, cfg, f"temp_{uuid.uuid4().hex[:8]}", save=False
        )
    except AnalysisError as exc:
        raise HTTPException(status_code=500, detail=f"Reference analysis failed: {exc}")

    converter = VoiceConverter(cfg)
    try:
        converted, report = converter.convert_voice(src_audio, src_sr, temp_profile, cfg)
    except Exception as exc:
        logger.exception("Conversion failed")
        raise HTTPException(status_code=500, detail=f"Conversion error: {exc}")

    wav_bytes = _audio_to_wav_bytes(converted, src_sr)
    return StreamingResponse(
        io.BytesIO(wav_bytes),
        media_type="audio/wav",
        headers={
            "Content-Disposition": "attachment; filename=converted.wav",
            "X-Conversion-Method": "voice_converter_v1_temp",
            "X-Processing-Time": f"{report.get('processing_time_sec', 0):.3f}s",
        },
    )


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api.main:app", host=HOST, port=PORT, reload=True)
