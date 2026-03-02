"""
VoiceAPI Unified Backend - FastAPI Server
Combines VoiceAPI (VITS) and Sarvam.ai TTS with unified REST API.

Strategy:
  - For all synthesis requests, VoiceAPI is tried FIRST if it supports the language.
  - If VoiceAPI fails (any error) AND Sarvam supports the language, Sarvam is used.
  - If the user explicitly picks 'sarvam', Sarvam is used directly (no VoiceAPI attempt).
  - If the user explicitly picks 'voiceapi', VoiceAPI is used with Sarvam as fallback.
  - Default provider is 'auto' = VoiceAPI first, Sarvam as fallback.
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import Optional, Literal, List
from dotenv import load_dotenv
import logging
import os
import io
from datetime import datetime

from voiceapi_client import VoiceAPIClient, VoiceAPIError
from sarvam_client import SarvamClient, SarvamAPIError

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Get environment variables
SARVAM_API_KEY = os.getenv('SARVAM_API_KEY', '')
VOICEAPI_BASE_URL = os.getenv('VOICEAPI_BASE_URL', 'https://harshil748-voiceapi.hf.space')
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5500').split(',')
HOST = os.getenv('HOST', '0.0.0.0')
PORT = int(os.getenv('PORT', '8001'))
API_TIMEOUT = int(os.getenv('API_TIMEOUT', '60'))

# =============================================================================
# Initialize API clients  (must come before lifespan definition)
# =============================================================================

logger.info("Initializing API clients...")
voice_api = VoiceAPIClient(base_url=VOICEAPI_BASE_URL, timeout=API_TIMEOUT)

# Initialize Sarvam client (handle missing API key gracefully)
sarvam_api = None
if SARVAM_API_KEY and SARVAM_API_KEY != 'your_sarvam_api_key_here':
    try:
        sarvam_api = SarvamClient(api_key=SARVAM_API_KEY, timeout=API_TIMEOUT)
        logger.info("✅ Sarvam API client initialized")
    except ValueError as e:
        logger.warning(f"⚠️  Sarvam API not available: {e}")
else:
    logger.warning("⚠️  Sarvam API key not configured. Only VoiceAPI will be available.")


# =============================================================================
# Lifespan (startup / shutdown) — must be defined before app = FastAPI(...)
# =============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown."""
    # --- Startup ---
    logger.info("=" * 60)
    logger.info("🚀 VoiceAPI Unified Backend Starting...")
    logger.info("=" * 60)
    logger.info(f"VoiceAPI Endpoint : {VOICEAPI_BASE_URL}")
    logger.info(f"Sarvam API        : {'✅ Configured' if SARVAM_API_KEY and SARVAM_API_KEY != 'your_sarvam_api_key_here' else '❌ Not configured'}")
    logger.info(f"CORS Origins      : {CORS_ORIGINS}")
    logger.info(f"Server            : http://{HOST}:{PORT}")
    logger.info(f"API Docs          : http://{HOST}:{PORT}/docs")
    logger.info("Strategy          : VoiceAPI first → Sarvam fallback")
    logger.info("=" * 60)
    yield
    # --- Shutdown ---
    logger.info("Shutting down API clients...")
    await voice_api.close()
    if sarvam_api:
        await sarvam_api.close()
    logger.info("✅ Shutdown complete")


# =============================================================================
# Create FastAPI app  (lifespan is now defined above, so no NameError)
# =============================================================================

app = FastAPI(
    title="VoiceAPI Unified Backend",
    description=(
        "Unified TTS API combining VoiceAPI (VITS) and Sarvam.ai.\n"
        "Strategy: VoiceAPI is always tried first; Sarvam is the automatic fallback."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Configure CORS
# allow_origins=["*"] covers localhost, 127.0.0.1, and file:// (Origin: null)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =============================================================================
# Pydantic Models
# =============================================================================

class SynthesizeRequest(BaseModel):
    """
    Request model for speech synthesis.

    provider:
      'auto'    → Try VoiceAPI first; fall back to Sarvam if VoiceAPI fails (default)
      'voiceapi'→ Prefer VoiceAPI; fall back to Sarvam on failure
      'sarvam'  → Use Sarvam directly (no VoiceAPI attempt)
    """
    text: str = Field(..., min_length=1, max_length=2500, description="Text to synthesize")
    language: str = Field(..., description="Language name (e.g. 'hindi', 'english')")
    provider: Literal["auto", "voiceapi", "sarvam"] = Field(
        "auto",
        description="TTS provider. 'auto' = VoiceAPI first, Sarvam fallback."
    )
    speaker: Optional[str] = Field("meera", description="AI voice ID (Premium only)")
    pace: float = Field(1.0, ge=0.5, le=2.0, description="Speech pace/speed (0.5–2.0)")
    pitch: int = Field(
        0, ge=-10, le=10,
        description="Voice pitch offset (-10 to +10). 0 = normal."
    )
    enable_preprocessing: bool = Field(True, description="Enable text normalization")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str
    voiceapi_available: bool
    sarvam_available: bool
    message: Optional[str] = None


class LanguageInfo(BaseModel):
    """Language support information"""
    code: str
    name: str
    voiceapi_supported: bool
    sarvam_supported: bool
    sarvam_code: Optional[str] = None


class SpeakerInfo(BaseModel):
    """Speaker information"""
    id: str
    name: str
    gender: str
    language: str


# =============================================================================
# Language Mapping
# =============================================================================

# Map common language names to VoiceAPI and Sarvam codes
LANGUAGE_MAPPING = {
    'hindi': {'voiceapi': 'hindi', 'sarvam': 'hi-IN', 'name': 'Hindi (हिन्दी)'},
    'bengali': {'voiceapi': 'bengali', 'sarvam': 'bn-IN', 'name': 'Bengali (বাংলা)'},
    'english': {'voiceapi': 'english', 'sarvam': 'en-IN', 'name': 'Indian English'},
    'gujarati': {'voiceapi': 'gujarati', 'sarvam': 'gu-IN', 'name': 'Gujarati (ગુજરાતી)'},
    'marathi': {'voiceapi': 'marathi', 'sarvam': 'mr-IN', 'name': 'Marathi (मराठी)'},
    'telugu': {'voiceapi': 'telugu', 'sarvam': 'te-IN', 'name': 'Telugu (తెలుగు)'},
    'kannada': {'voiceapi': 'kannada', 'sarvam': 'kn-IN', 'name': 'Kannada (ಕನ್ನಡ)'},
    'tamil': {'voiceapi': None, 'sarvam': 'ta-IN', 'name': 'Tamil (தமிழ்)'},
    'malayalam': {'voiceapi': None, 'sarvam': 'ml-IN', 'name': 'Malayalam (മലയാളം)'},
    'punjabi': {'voiceapi': None, 'sarvam': 'pa-IN', 'name': 'Punjabi (ਪੰਜਾਬੀ)'},
    'odia': {'voiceapi': None, 'sarvam': 'or-IN', 'name': 'Odia (ଓଡ଼ିଆ)'},
    'bhojpuri': {'voiceapi': 'bhojpuri', 'sarvam': None, 'name': 'Bhojpuri'},
    'chhattisgarhi': {'voiceapi': 'chhattisgarhi', 'sarvam': None, 'name': 'Chhattisgarhi'},
    'maithili': {'voiceapi': 'maithili', 'sarvam': None, 'name': 'Maithili'},
    'magahi': {'voiceapi': 'magahi', 'sarvam': None, 'name': 'Magahi'},
}


# =============================================================================
# API Endpoints
# =============================================================================

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "VoiceAPI Unified Backend",
        "version": "1.0.0",
        "description": "Unified TTS API combining VoiceAPI and Sarvam.ai",
        "docs": "/docs",
        "health": "/api/health",
        "endpoints": {
            "health": "GET /api/health",
            "languages": "GET /api/languages",
            "speakers": "GET /api/speakers",
            "synthesize": "POST /api/synthesize"
        }
    }


@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """
    Check health status of both TTS providers.
    Returns availability status for VoiceAPI and Sarvam.ai.
    """
    logger.info("Health check requested")
    
    # Check VoiceAPI availability
    voiceapi_available = await voice_api.check_health()
    
    # Check Sarvam API availability
    sarvam_available = False
    if sarvam_api:
        sarvam_available = await sarvam_api.check_health()
    
    # Determine overall status
    if voiceapi_available or sarvam_available:
        status = "healthy"
        message = "At least one TTS provider is available"
    else:
        status = "degraded"
        message = "All TTS providers are currently unavailable"
    
    return HealthResponse(
        status=status,
        timestamp=datetime.now().isoformat(),
        voiceapi_available=voiceapi_available,
        sarvam_available=sarvam_available,
        message=message
    )


@app.get("/api/languages", response_model=List[LanguageInfo])
async def get_languages():
    """
    Get list of supported languages with provider availability.
    Returns unified language list showing which providers support each language.
    """
    logger.info("Languages list requested")
    
    languages = []
    for code, info in LANGUAGE_MAPPING.items():
        languages.append(LanguageInfo(
            code=code,
            name=info['name'],
            voiceapi_supported=info['voiceapi'] is not None,
            sarvam_supported=info['sarvam'] is not None and sarvam_api is not None,
            sarvam_code=info['sarvam']
        ))
    
    return languages


@app.get("/api/speakers", response_model=List[SpeakerInfo])
async def get_speakers():
    """
    Get list of available speakers (Sarvam.ai voices).
    Returns empty list if Sarvam.ai is not configured.
    """
    logger.info("Speakers list requested")
    
    if not sarvam_api:
        return []
    
    speakers = [
        SpeakerInfo(**speaker)
        for speaker in SarvamClient.get_supported_speakers()
    ]
    
    return speakers


@app.post("/api/synthesize")
async def synthesize_speech(request: SynthesizeRequest):
    """
    Synthesize speech from text.

    Routing strategy
    ----------------
    'auto' or 'voiceapi'  →  VoiceAPI attempted first.
                              If VoiceAPI fails AND Sarvam supports the language,
                              Sarvam is used automatically as fallback.

    'sarvam'              →  Sarvam used directly (no VoiceAPI attempt).

    Returns WAV (VoiceAPI) or MP3 (Sarvam) as a streaming audio response.
    """
    logger.info(
        f"Synthesis request | provider={request.provider} | "
        f"lang={request.language} | text_len={len(request.text)}"
    )

    # ---- Validate language ----
    if request.language not in LANGUAGE_MAPPING:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported language: '{request.language}'. "
                f"Available: {', '.join(LANGUAGE_MAPPING.keys())}"
            ),
        )

    lang_info = LANGUAGE_MAPPING[request.language]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    # Convert pitch offset (-10..10) to VoiceAPI pitch multiplier (0.5..2.0)
    # -10 → 0.5, 0 → 1.0, 10 → 1.5  (clamped to [0.5, 2.0])
    voiceapi_pitch = max(0.5, min(2.0, 1.0 + request.pitch * 0.05))

    # -----------------------------------------------------------------------
    # Helper: synthesize via VoiceAPI
    # -----------------------------------------------------------------------
    async def try_voiceapi() -> Optional[Response]:
        """Attempt synthesis with VoiceAPI. Returns Response or None on failure."""
        if not lang_info['voiceapi']:
            logger.info(f"VoiceAPI does not support '{request.language}' — skipping")
            return None
        try:
            audio_data = await voice_api.synthesize(
                text=request.text,
                language=lang_info['voiceapi'],
                speed=request.pace,
                pitch=voiceapi_pitch,
                energy=1.0,
                normalize=request.enable_preprocessing,
            )
            logger.info(f"✅ VoiceAPI synthesis succeeded ({len(audio_data)} bytes)")
            return Response(
                content=audio_data,
                media_type="audio/wav",
                headers={
                    "Content-Disposition": f'inline; filename="speech_{timestamp}.wav"',
                    "X-Provider": "voiceapi",
                    "X-Language": request.language,
                    "X-Model": "VITS",
                },
            )
        except VoiceAPIError as exc:
            logger.warning(f"VoiceAPI synthesis failed: {exc}")
            return None

    # -----------------------------------------------------------------------
    # Helper: synthesize via Sarvam
    # -----------------------------------------------------------------------
    async def try_sarvam(reason: str = "") -> Response:
        """
        Attempt synthesis with Sarvam.ai.
        Raises HTTPException if Sarvam is unavailable or language not supported.
        """
        if not sarvam_api:
            raise HTTPException(
                status_code=503,
                detail=(
                    "Sarvam.ai is not configured (SARVAM_API_KEY missing in .env). "
                    + (f"VoiceAPI also failed: {reason}" if reason else "")
                ),
            )
        if not lang_info['sarvam']:
            raise HTTPException(
                status_code=400,
                detail=(
                    f"{lang_info['name']} is not supported by Sarvam.ai either. "
                    "This language is only available via VoiceAPI."
                    + (f" VoiceAPI error: {reason}" if reason else "")
                ),
            )
        try:
            audio_data = await sarvam_api.text_to_speech(
                text=request.text,
                language_code=lang_info['sarvam'],
                speaker=request.speaker or "meera",
                pace=request.pace,
                pitch=request.pitch,
                enable_preprocessing=request.enable_preprocessing,
            )
            logger.info(
                f"✅ Sarvam synthesis succeeded ({len(audio_data)} bytes)"
                + (f" [fallback from VoiceAPI: {reason}]" if reason else "")
            )
            return Response(
                content=audio_data,
                media_type="audio/mp3",
                headers={
                    "Content-Disposition": f'inline; filename="speech_{timestamp}.mp3"',
                    "X-Provider": "sarvam",
                    "X-Language": request.language,
                    "X-Speaker": request.speaker or "meera",
                    "X-Model": "bulbul:v3",
                    "X-Fallback": "true" if reason else "false",
                },
            )
        except SarvamAPIError as exc:
            err = str(exc)
            if "rate limit" in err.lower():
                raise HTTPException(status_code=429, detail=err)
            if "invalid api key" in err.lower() or "401" in err:
                raise HTTPException(status_code=401, detail=err)
            if "timeout" in err.lower():
                raise HTTPException(status_code=504, detail=err)
            raise HTTPException(status_code=500, detail=err)

    # -----------------------------------------------------------------------
    # Routing logic
    # -----------------------------------------------------------------------
    try:
        if request.provider == "sarvam":
            # Explicit Sarvam request — no VoiceAPI attempt
            return await try_sarvam()

        else:
            # 'auto' or 'voiceapi': try VoiceAPI first
            result = await try_voiceapi()
            if result is not None:
                return result  # VoiceAPI succeeded

            # VoiceAPI failed (or unsupported language) — try Sarvam as fallback
            voiceapi_failure = "VoiceAPI unavailable or failed"
            logger.info(f"Falling back to Sarvam.ai for '{request.language}'")
            return await try_sarvam(reason=voiceapi_failure)

    except HTTPException:
        raise  # pass through already-formatted HTTP errors
    except Exception as exc:
        logger.error(f"Unexpected synthesis error: {exc}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal server error: {exc}")


# =============================================================================
# Main Entry Point
# =============================================================================

if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting server on {HOST}:{PORT}...")
    
    uvicorn.run(
        app,
        host=HOST,
        port=PORT,
        log_level="info",
        access_log=True
    )
