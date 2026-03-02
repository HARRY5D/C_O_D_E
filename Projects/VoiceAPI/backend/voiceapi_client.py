"""
VoiceAPI Client - Wrapper for the VITS-based VoiceAPI
Correctly implements the API according to official documentation.

API Base: https://harshil748-voiceapi.hf.space

Key Endpoints:
  POST /synthesize      - JSON body, voice key like "hi_male"
  POST /Get_Inference   - text+lang as QUERY PARAMS, speaker_wav as multipart body
  GET  /health          - health status
  GET  /voices          - list available voices
  GET  /languages       - list supported languages
"""

import httpx
import io
import logging
import struct
from typing import Optional, List, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class VoiceAPIError(Exception):
    """Custom exception for VoiceAPI errors"""
    pass


def _extract_detail(response: httpx.Response) -> str:
    """Extract a readable error string from an httpx response body."""
    try:
        data = response.json()
        if isinstance(data, dict) and 'detail' in data:
            detail = data['detail']
            if isinstance(detail, list):
                return '; '.join(
                    f"{err.get('loc', '')}: {err.get('msg', '')}"
                    for err in detail
                )
            return str(detail)
    except Exception:
        pass
    return response.text[:300]


class VoiceAPIClient:
    """
    Client for the VITS-based VoiceAPI (harshil748-voiceapi.hf.space).
    Supports 10 Indian languages + English with male/female voices.

    Primary synthesis: POST /synthesize  (JSON body, voice key e.g. "hi_male")
    Fallback synthesis: POST /Get_Inference (text+lang as query params,
                                              speaker_wav as multipart file)
    """

    # Languages accepted by the /Get_Inference `lang` query param
    SUPPORTED_LANGUAGES = [
        'hindi', 'bengali', 'english', 'gujarati', 'marathi',
        'telugu', 'kannada', 'bhojpuri', 'chhattisgarhi',
        'maithili', 'magahi'
    ]

    # Static mapping: language name → default voice key for /synthesize
    # Voice key format: {lang_code}_{gender}  (e.g. hi_male)
    VOICE_MAPPING: Dict[str, str] = {
        'hindi':         'hi_male',
        'bengali':       'bn_male',
        'english':       'en_male',
        'gujarati':      'gu_male',
        'marathi':       'mr_male',
        'telugu':        'te_male',
        'kannada':       'kn_male',
        'bhojpuri':      'bh_male',
        'chhattisgarhi': 'cg_male',
        'maithili':      'mai_male',
        'magahi':        'mag_male',
    }

    def __init__(self, base_url: str, timeout: int = 60):
        """
        Initialize the VoiceAPI client.

        Args:
            base_url: Base URL of the VoiceAPI endpoint
            timeout:  Request timeout in seconds (default: 60)
        """
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
        self.client = httpx.AsyncClient(
            timeout=httpx.Timeout(timeout),
            follow_redirects=True
        )
        self._voices_cache: Optional[List[Dict]] = None
        logger.info(f"VoiceAPIClient initialized: {self.base_url}")

    # ------------------------------------------------------------------
    # Public synthesis interface
    # ------------------------------------------------------------------

    async def synthesize(
        self,
        text: str,
        language: str,
        speed: float = 1.0,
        pitch: float = 1.0,
        energy: float = 1.0,
        normalize: bool = True,
    ) -> bytes:
        """
        Synthesize speech. Tries /synthesize (JSON) first; falls back to
        /Get_Inference (multipart + query params) on failure.

        Args:
            text:      Input text to synthesize
            language:  Language name (e.g. 'hindi', 'english')
            speed:     Speech speed 0.5–2.0 (default 1.0)
            pitch:     Voice pitch 0.5–2.0 (default 1.0)
            energy:    Voice energy 0.5–2.0 (default 1.0)
            normalize: Enable text normalization (default True)

        Returns:
            bytes: Synthesized audio in WAV format

        Raises:
            VoiceAPIError: If both /synthesize and /Get_Inference fail
        """
        if not text or not text.strip():
            raise VoiceAPIError("Text cannot be empty")

        lang = language.lower()
        if lang not in self.SUPPORTED_LANGUAGES:
            raise VoiceAPIError(
                f"Language '{language}' is not supported by VoiceAPI. "
                f"Supported: {', '.join(self.SUPPORTED_LANGUAGES)}"
            )

        # --- Primary: /synthesize (JSON, no WAV file needed) ---
        primary_err: Optional[Exception] = None
        try:
            return await self._synthesize_json(text, lang, speed, pitch, energy, normalize)
        except VoiceAPIError as exc:
            primary_err = exc
            logger.warning(
                f"/synthesize failed ({exc}). Falling back to /Get_Inference..."
            )

        # --- Fallback: /Get_Inference (query params + multipart) ---
        try:
            return await self._synthesize_get_inference(text, lang)
        except VoiceAPIError as fallback_err:
            logger.error(f"/Get_Inference also failed: {fallback_err}")
            raise VoiceAPIError(
                f"VoiceAPI synthesis failed. "
                f"Primary error: {primary_err}. "
                f"Fallback error: {fallback_err}"
            )

    # ------------------------------------------------------------------
    # Private: /synthesize  (clean JSON endpoint)
    # ------------------------------------------------------------------

    async def _synthesize_json(
        self,
        text: str,
        language: str,
        speed: float,
        pitch: float,
        energy: float,
        normalize: bool,
    ) -> bytes:
        """
        POST /synthesize with JSON body.
        Uses voice key mapping (e.g. hindi → hi_male).
        """
        # Resolve voice key
        voice_key = self.VOICE_MAPPING.get(language)
        if not voice_key:
            voices = await self._fetch_voices_cached()
            for v in voices:
                lc = v.get('language_code', '').lower()
                if lc.startswith(language[:2]):
                    voice_key = v['key']
                    break
            if not voice_key:
                raise VoiceAPIError(
                    f"No voice key found for language '{language}'. "
                    f"Check /voices endpoint."
                )

        payload = {
            "text": text,
            "voice": voice_key,
            "speed": round(speed, 2),
            "pitch": round(pitch, 2),
            "energy": round(energy, 2),
            "normalize": normalize,
        }

        logger.info(f"POST /synthesize | voice={voice_key} | text_len={len(text)}")

        try:
            response = await self.client.post(
                f"{self.base_url}/synthesize",
                json=payload,
            )

            if response.status_code == 200:
                audio = response.content
                if len(audio) < 44:  # WAV header minimum
                    raise VoiceAPIError("Response too small to be a valid WAV file")
                logger.info(f"/synthesize ✅  {len(audio)} bytes")
                return audio

            elif response.status_code == 422:
                raise VoiceAPIError(
                    f"Validation error from /synthesize: {_extract_detail(response)}"
                )
            else:
                raise VoiceAPIError(
                    f"/synthesize HTTP {response.status_code}: {response.text[:200]}"
                )

        except httpx.TimeoutException:
            raise VoiceAPIError("/synthesize timed out")
        except httpx.NetworkError as exc:
            raise VoiceAPIError(f"/synthesize network error: {exc}")
        except VoiceAPIError:
            raise
        except Exception as exc:
            raise VoiceAPIError(f"/synthesize unexpected error: {exc}")

    # ------------------------------------------------------------------
    # Private: /Get_Inference  (hackathon spec, multipart)
    # ------------------------------------------------------------------

    async def _synthesize_get_inference(
        self,
        text: str,
        language: str,
        speaker_wav: Optional[bytes] = None,
    ) -> bytes:
        """
        POST /Get_Inference (hackathon API spec).

        Per official documentation:
          text        → URL QUERY PARAMETER  (NOT form field)
          lang        → URL QUERY PARAMETER  (NOT form field)
          speaker_wav → multipart/form-data file  (REQUIRED)
        """
        if speaker_wav is None:
            speaker_wav = self._create_default_wav()

        logger.info(
            f"POST /Get_Inference?text=...&lang={language} | text_len={len(text)}"
        )

        try:
            response = await self.client.post(
                f"{self.base_url}/Get_Inference",
                params={"text": text, "lang": language},           # ← query params
                files={"speaker_wav": ("ref.wav", speaker_wav, "audio/wav")},  # ← multipart
            )

            if response.status_code == 200:
                audio = response.content
                if len(audio) < 44:
                    raise VoiceAPIError("Response too small to be a valid WAV file")
                logger.info(f"/Get_Inference ✅  {len(audio)} bytes")
                return audio

            elif response.status_code == 422:
                raise VoiceAPIError(
                    f"Validation error from /Get_Inference: {_extract_detail(response)}"
                )
            else:
                raise VoiceAPIError(
                    f"/Get_Inference HTTP {response.status_code}: {response.text[:200]}"
                )

        except httpx.TimeoutException:
            raise VoiceAPIError("/Get_Inference timed out")
        except httpx.NetworkError as exc:
            raise VoiceAPIError(f"/Get_Inference network error: {exc}")
        except VoiceAPIError:
            raise
        except Exception as exc:
            raise VoiceAPIError(f"/Get_Inference unexpected error: {exc}")

    # ------------------------------------------------------------------
    # Voice / language discovery from live API
    # ------------------------------------------------------------------

    async def list_voices(self) -> List[Dict]:
        """
        Fetch available voices from GET /voices.

        Returns:
            list of dicts: {key, name, language_code, gender, loaded, downloaded, model_type}
        """
        try:
            response = await self.client.get(f"{self.base_url}/voices")
            if response.status_code == 200:
                return response.json()
            logger.warning(f"/voices returned HTTP {response.status_code}")
        except Exception as exc:
            logger.warning(f"Could not fetch /voices: {exc}")
        return []

    async def list_languages(self) -> List[str]:
        """
        Fetch supported language list from GET /languages.

        Returns:
            list of language name strings
        """
        try:
            response = await self.client.get(f"{self.base_url}/languages")
            if response.status_code == 200:
                data = response.json()
                if isinstance(data, list):
                    return data
        except Exception as exc:
            logger.warning(f"Could not fetch /languages: {exc}")
        return self.SUPPORTED_LANGUAGES.copy()

    async def _fetch_voices_cached(self) -> List[Dict]:
        """Return cached voices; hit /voices only once per client lifetime."""
        if self._voices_cache is None:
            self._voices_cache = await self.list_voices()
        return self._voices_cache

    # ------------------------------------------------------------------
    # Health check
    # ------------------------------------------------------------------

    async def check_health(self) -> bool:
        """
        Check VoiceAPI availability via GET /health.

        Returns:
            bool: True if the API is healthy
        """
        try:
            response = await self.client.get(
                f"{self.base_url}/health",
                timeout=httpx.Timeout(10),
            )
            is_healthy = response.status_code == 200
            logger.info(f"VoiceAPI health: {'✅ OK' if is_healthy else '❌ DOWN'}")
            return is_healthy
        except Exception as exc:
            logger.warning(f"VoiceAPI health check failed: {exc}")
            return False

    # ------------------------------------------------------------------
    # WAV helper
    # ------------------------------------------------------------------

    @staticmethod
    def _create_default_wav() -> bytes:
        """
        Build a minimal valid silent WAV file (1 second, 22050 Hz, mono 16-bit).
        Used as the mandatory speaker_wav for /Get_Inference.
        """
        sample_rate = 22050
        num_samples = sample_rate  # 1-second
        buf = io.BytesIO()
        # RIFF header
        buf.write(b'RIFF')
        buf.write(struct.pack('<I', 36 + num_samples * 2))
        buf.write(b'WAVE')
        # fmt chunk
        buf.write(b'fmt ')
        buf.write(struct.pack('<I', 16))          # chunk size
        buf.write(struct.pack('<H', 1))           # PCM
        buf.write(struct.pack('<H', 1))           # mono
        buf.write(struct.pack('<I', sample_rate))
        buf.write(struct.pack('<I', sample_rate * 2))  # byte rate
        buf.write(struct.pack('<H', 2))           # block align
        buf.write(struct.pack('<H', 16))          # bits per sample
        # data chunk
        buf.write(b'data')
        buf.write(struct.pack('<I', num_samples * 2))
        buf.write(b'\x00\x00' * num_samples)      # silence
        return buf.getvalue()

    # ------------------------------------------------------------------
    # Lifecycle
    # ------------------------------------------------------------------

    async def close(self):
        """Close the underlying HTTP client."""
        await self.client.aclose()
        logger.info("VoiceAPI client closed")

    def __del__(self):
        try:
            import asyncio
            if hasattr(self, 'client') and not self.client.is_closed:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    loop.create_task(self.client.aclose())
        except Exception:
            pass
