"""
Sarvam.ai Client - Wrapper for Sarvam.ai Text-to-Speech API
Provides high-quality multilingual TTS with multiple speakers.
"""

import httpx
import base64
import logging
from typing import Optional, AsyncIterator, Dict

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class SarvamAPIError(Exception):
    """Custom exception for Sarvam API errors"""
    pass


class SarvamClient:
    """
    Client for Sarvam.ai Text-to-Speech API.
    Supports 11+ Indian languages with 35+ natural-sounding speakers.
    """
    
    # Base URL for Sarvam.ai API
    BASE_URL = "https://api.sarvam.ai"
    
    # Supported language codes (ISO format)
    SUPPORTED_LANGUAGES = {
        'hi-IN': 'Hindi (हिन्दी)',
        'bn-IN': 'Bengali (বাংলা)',
        'en-IN': 'Indian English',
        'ta-IN': 'Tamil (தமிழ்)',
        'te-IN': 'Telugu (తెలుగు)',
        'kn-IN': 'Kannada (ಕನ್ನಡ)',
        'ml-IN': 'Malayalam (മലയാളം)',
        'mr-IN': 'Marathi (मराठी)',
        'gu-IN': 'Gujarati (ગુજરાતી)',
        'pa-IN': 'Punjabi (ਪੰਜਾਬੀ)',
        'or-IN': 'Odia (ଓଡ଼ିଆ)'
    }
    
    # Available speakers with metadata
    SUPPORTED_SPEAKERS = [
        {'id': 'meera', 'name': 'Meera', 'gender': 'female', 'language': 'Hindi'},
        {'id': 'arvind', 'name': 'Arvind', 'gender': 'male', 'language': 'Hindi'},
        {'id': 'nisha', 'name': 'Nisha', 'gender': 'female', 'language': 'Hindi'},
        {'id': 'ravi', 'name': 'Ravi', 'gender': 'male', 'language': 'Hindi'},
        {'id': 'priya', 'name': 'Priya', 'gender': 'female', 'language': 'Multi'},
        {'id': 'amit', 'name': 'Amit', 'gender': 'male', 'language': 'Multi'},
        {'id': 'shubh', 'name': 'Shubh', 'gender': 'male', 'language': 'Multi'},
        {'id': 'sangeeta', 'name': 'Sangeeta', 'gender': 'female', 'language': 'Multi'},
    ]
    
    def __init__(self, api_key: str, timeout: int = 60):
        """
        Initialize Sarvam API client.
        
        Args:
            api_key: Sarvam.ai API subscription key
            timeout: Request timeout in seconds (default: 60)
        
        Raises:
            ValueError: If API key is empty
        """
        if not api_key or api_key.strip() == "" or api_key == "your_sarvam_api_key_here":
            raise ValueError(
                "Invalid Sarvam API key. Please set SARVAM_API_KEY in .env file. "
                "Get your key from: https://www.sarvam.ai/"
            )
        
        self.api_key = api_key.strip()
        self.timeout = timeout
        
        # Create HTTP client with authentication headers
        self.client = httpx.AsyncClient(
            base_url=self.BASE_URL,
            headers={
                'api-subscription-key': self.api_key,
                'Content-Type': 'application/json'
            },
            timeout=httpx.Timeout(timeout),
            follow_redirects=True
        )
        
        logger.info("Sarvam API client initialized")
    
    async def text_to_speech(
        self,
        text: str,
        language_code: str,
        speaker: str = "meera",
        pace: float = 1.0,
        pitch: float = 0.0,
        enable_preprocessing: bool = True
    ) -> bytes:
        """
        Convert text to speech using Sarvam.ai API.
        
        Args:
            text: Input text to synthesize
            language_code: Language code (e.g., 'hi-IN', 'en-IN')
            speaker: Speaker voice ID (default: 'meera')
            pace: Speech pace/speed (0.5-2.0, default: 1.0)
            pitch: Voice pitch adjustment (-10 to 10, default: 0)
            enable_preprocessing: Enable text preprocessing (default: True)
        
        Returns:
            bytes: Audio data in MP3 format
        
        Raises:
            SarvamAPIError: If API request fails
        """
        # Validate inputs
        if not text or not text.strip():
            raise SarvamAPIError("Text cannot be empty")
        
        if language_code not in self.SUPPORTED_LANGUAGES:
            raise SarvamAPIError(
                f"Language '{language_code}' not supported. "
                f"Use one of: {', '.join(self.SUPPORTED_LANGUAGES.keys())}"
            )
        
        if pace < 0.5 or pace > 2.0:
            raise SarvamAPIError("Pace must be between 0.5 and 2.0")
        
        if pitch < -10 or pitch > 10:
            raise SarvamAPIError("Pitch must be between -10 and 10")
        
        # Prepare request payload
        payload = {
            "inputs": [text],
            "target_language_code": language_code,
            "speaker": speaker,
            "model": "bulbul:v3",  # Sarvam's latest TTS model
            "pace": pace,
            "pitch": pitch,
            "loudness": 1.5,
            "speech_sample_rate": 22050,
            "enable_preprocessing": enable_preprocessing,
            "output_audio_codec": "mp3"
        }
        
        try:
            logger.info(
                f"Sarvam TTS: lang={language_code}, speaker={speaker}, "
                f"text_len={len(text)}"
            )
            
            # Make API request
            response = await self.client.post(
                "/text-to-speech",
                json=payload
            )
            
            # Handle different status codes
            if response.status_code == 200:
                # Parse response
                response_data = response.json()
                
                # Extract and decode base64 audio
                if 'audios' in response_data and len(response_data['audios']) > 0:
                    audio_base64 = response_data['audios'][0]
                    audio_bytes = base64.b64decode(audio_base64)
                    
                    logger.info(f"Sarvam synthesis successful: {len(audio_bytes)} bytes")
                    return audio_bytes
                else:
                    raise SarvamAPIError("No audio data in response")
            
            elif response.status_code == 401:
                logger.error("Sarvam API authentication failed")
                raise SarvamAPIError(
                    "Invalid API key. Please check your SARVAM_API_KEY in .env file."
                )
            
            elif response.status_code == 429:
                logger.error("Sarvam API rate limit exceeded")
                raise SarvamAPIError(
                    "Rate limit exceeded. Please wait a moment and try again. "
                    "Consider upgrading your Sarvam.ai plan for higher limits."
                )
            
            elif response.status_code == 400:
                error_msg = response.json().get('detail', 'Invalid request')
                logger.error(f"Sarvam API validation error: {error_msg}")
                raise SarvamAPIError(f"Invalid request: {error_msg}")
            
            elif response.status_code == 500:
                logger.error("Sarvam API server error")
                raise SarvamAPIError("Sarvam.ai server error. Please try again.")
            
            else:
                logger.error(f"Unexpected Sarvam status: {response.status_code}")
                raise SarvamAPIError(
                    f"Sarvam.ai returned status {response.status_code}"
                )
        
        except httpx.TimeoutException:
            logger.error("Sarvam API request timeout")
            raise SarvamAPIError(
                "Request timeout. The text might be too long or "
                "the service is slow. Please try again."
            )
        
        except httpx.NetworkError as e:
            logger.error(f"Sarvam network error: {e}")
            raise SarvamAPIError(
                "Cannot connect to Sarvam.ai. Please check your internet connection."
            )
        
        except SarvamAPIError:
            # Re-raise our custom errors
            raise
        
        except Exception as e:
            logger.error(f"Unexpected Sarvam error: {e}", exc_info=True)
            raise SarvamAPIError(f"Synthesis failed: {str(e)}")
    
    async def text_to_speech_stream(
        self,
        text: str,
        language_code: str,
        speaker: str = "meera",
        pace: float = 1.0,
        pitch: float = 0.0,
        enable_preprocessing: bool = True
    ) -> AsyncIterator[bytes]:
        """
        Convert text to speech with streaming response.
        Yields audio chunks as they are generated.
        
        Args:
            Same as text_to_speech()
        
        Yields:
            bytes: Audio chunks
        
        Raises:
            SarvamAPIError: If API request fails
        """
        # Note: Streaming endpoint might require different Sarvam.ai plan
        # This is a placeholder for future implementation
        
        payload = {
            "inputs": [text],
            "target_language_code": language_code,
            "speaker": speaker,
            "model": "bulbul:v3",
            "pace": pace,
            "pitch": pitch,
            "loudness": 1.5,
            "speech_sample_rate": 22050,
            "enable_preprocessing": enable_preprocessing,
            "output_audio_codec": "mp3"
        }
        
        try:
            async with self.client.stream(
                'POST',
                '/text-to-speech/stream',
                json=payload
            ) as response:
                if response.status_code == 200:
                    async for chunk in response.aiter_bytes():
                        yield chunk
                else:
                    raise SarvamAPIError(
                        f"Stream request failed with status {response.status_code}"
                    )
        
        except Exception as e:
            logger.error(f"Streaming error: {e}", exc_info=True)
            raise SarvamAPIError(f"Streaming failed: {str(e)}")
    
    async def check_health(self) -> bool:
        """
        Check if Sarvam.ai API is reachable.

        Uses a lightweight HEAD request to avoid wasting API credits.
        A 200, 401, 403, or 405 response all confirm the server is UP
        (auth errors mean it's reachable; 405 = method not allowed but alive).

        Returns:
            bool: True if API is reachable, False otherwise
        """
        try:
            response = await self.client.head(
                "/text-to-speech",
                timeout=httpx.Timeout(10),
            )
            # Any HTTP response (including 4xx) confirms the endpoint exists
            is_healthy = response.status_code < 500
            logger.info(f"Sarvam API health check: {'✅ OK' if is_healthy else '❌ DOWN'} (HTTP {response.status_code})")
            return is_healthy
        except Exception as e:
            logger.warning(f"Sarvam API health check failed: {e}")
            return False
    
    @classmethod
    def get_supported_languages(cls) -> Dict[str, str]:
        """Get dictionary of supported language codes and names"""
        return cls.SUPPORTED_LANGUAGES.copy()
    
    @classmethod
    def get_supported_speakers(cls) -> list:
        """Get list of supported speakers"""
        return cls.SUPPORTED_SPEAKERS.copy()
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
        logger.info("Sarvam API client closed")
    
    def __del__(self):
        """Cleanup on deletion"""
        try:
            if hasattr(self, 'client'):
                import asyncio
                asyncio.create_task(self.client.aclose())
        except:
            pass
