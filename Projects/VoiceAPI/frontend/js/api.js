/**
 * API Client for VoiceAPI Backend
 * Handles all communication with the backend server
 */

import CONFIG from './config.js';

/**
 * Unified API Client for TTS services
 * All requests go through the backend - no direct API calls to external services
 */
class UnifiedAPIClient {
  constructor() {
    this.baseURL = CONFIG.API_BASE_URL;
    this.languagesCache = null;
    this.speakersCache = null;
  }
  
  /**
   * Fetch list of supported languages
   * @returns {Promise<Array>} Array of language objects
   */
  async fetchLanguages() {
    // Return cached data if available
    if (this.languagesCache) {
      return this.languagesCache;
    }
    
    try {
      const response = await fetch(`${this.baseURL}/api/languages`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) {
        throw new Error(`Failed to fetch languages: ${response.statusText}`);
      }
      
      const languages = await response.json();
      this.languagesCache = languages; // Cache for future use
      return languages;
    } catch (error) {
      console.error('Error fetching languages:', error);
      throw new Error('Failed to load languages. Please check backend connection.');
    }
  }
  
  /**
   * Fetch list of available speakers
   * @returns {Promise<Array>} Array of speaker objects
   */
  async fetchSpeakers() {
    // Return cached data if available
    if (this.speakersCache) {
      return this.speakersCache;
    }
    
    try {
      const response = await fetch(`${this.baseURL}/api/speakers`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        }
      });
      
      if (!response.ok) {
        throw new Error(`Failed to fetch speakers: ${response.statusText}`);
      }
      
      const speakers = await response.json();
      this.speakersCache = speakers; // Cache for future use
      return speakers;
    } catch (error) {
      console.error('Error fetching speakers:', error);
      throw new Error('Failed to load speakers. Premium service may not be available.');
    }
  }
  
  /**
   * Check backend health status
   * @returns {Promise<Object>} Health status object
   */
  async checkHealth() {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), 10000); // 10 second timeout
      
      const response = await fetch(`${this.baseURL}/api/health`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json'
        },
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      if (!response.ok) {
        return { available: false, voiceapi_available: false, sarvam_available: false };
      }
      
      const health = await response.json();
      return health;
    } catch (error) {
      console.error('Health check failed:', error);
      return { available: false, voiceapi_available: false, sarvam_available: false };
    }
  }
  
  /**
   * Synthesize speech from text
   * @param {Object} params - Synthesis parameters
   * @param {string} params.text - Text to synthesize
   * @param {string} params.language - Language code
   * @param {string} params.provider - Provider ('voiceapi' or 'sarvam')
   * @param {string} [params.speaker] - Speaker voice (for sarvam)
   * @param {number} [params.pace] - Speech pace (0.5-2.0)
   * @param {number} [params.pitch] - Voice pitch (-10 to 10)
   * @param {boolean} [params.enable_preprocessing] - Enable preprocessing
   * @returns {Promise<Blob>} Audio blob
   */
  async synthesize(params) {
    // Validate parameters
    this.validateSynthesisParams(params);
    
    try {
      // Create abort controller for timeout
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), CONFIG.API_TIMEOUT);
      
      // Make request
      const response = await fetch(`${this.baseURL}/api/synthesize`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(params),
        signal: controller.signal
      });
      
      clearTimeout(timeoutId);
      
      // Handle errors
      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw await this.handleAPIError(response, errorData);
      }
      
      // Get audio blob
      const audioBlob = await response.blob();
      return audioBlob;
    } catch (error) {
      if (error.name === 'AbortError') {
        throw new Error('Request timeout. The text might be too long or the server is slow.');
      }
      throw error;
    }
  }
  
  /**
   * Validate synthesis parameters
   * @param {Object} params - Parameters to validate
   * @throws {Error} If validation fails
   */
  validateSynthesisParams(params) {
    // Check text
    if (!params.text || params.text.trim().length === 0) {
      throw new Error('Text cannot be empty');
    }
    
    if (params.text.length > CONFIG.MAX_TEXT_LENGTH) {
      throw new Error(`Text too long. Maximum ${CONFIG.MAX_TEXT_LENGTH} characters allowed.`);
    }
    
    // Check language
    if (!params.language) {
      throw new Error('Language must be specified');
    }
    
    // Check provider
    if (!['auto', 'voiceapi', 'sarvam'].includes(params.provider)) {
      throw new Error('Invalid provider. Must be "auto", "voiceapi", or "sarvam"');
    }
    
    // Check pace
    if (params.pace !== undefined) {
      const pace = parseFloat(params.pace);
      if (isNaN(pace) || pace < 0.5 || pace > 2.0) {
        throw new Error('Pace must be between 0.5 and 2.0');
      }
    }
    
    // Check pitch
    if (params.pitch !== undefined) {
      const pitch = parseInt(params.pitch);
      if (isNaN(pitch) || pitch < -10 || pitch > 10) {
        throw new Error('Pitch must be between -10 and 10');
      }
    }
  }
  
  /**
   * Handle API error responses
   * @param {Response} response - Fetch response object
   * @param {Object} errorData - Error data from response
   * @returns {Error} Formatted error
   */
  async handleAPIError(response, errorData) {
    const status = response.status;
    const detail = errorData.detail || response.statusText;
    
    switch (status) {
      case 400:
        return new Error(`Invalid request: ${detail}`);
      
      case 401:
        return new Error('API authentication failed. Please check backend configuration.');
      
      case 429:
        return new Error('Rate limit exceeded. Please wait a moment and try again.');
      
      case 500:
        return new Error(`Server error: ${detail}`);
      
      case 503:
        return new Error('Service unavailable. Please try again later or use a different provider.');
      
      case 504:
        return new Error('Request timeout. Please try with shorter text or try again later.');
      
      default:
        return new Error(`Request failed: ${detail}`);
    }
  }

  // ── Voice Converter API ──────────────────────────────────────────────────

  async converterHealth() {
    const response = await fetch(`${this.baseURL}/api/voice-converter/health`, {
      signal: AbortSignal.timeout(6000),
    });
    return response.json();
  }

  async createVoiceProfile(audioFile, profileName) {
    const form = new FormData();
    form.append('reference_audio', audioFile, audioFile.name);
    form.append('profile_name', profileName);
    const response = await fetch(`${this.baseURL}/api/voice-converter/create-profile`, {
      method: 'POST',
      body: form,
      signal: AbortSignal.timeout(120_000),
    });
    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: response.statusText }));
      throw new Error(err.detail || 'Failed to create voice profile');
    }
    return response.json();
  }

  async listVoiceProfiles() {
    const response = await fetch(`${this.baseURL}/api/voice-converter/profiles`);
    if (!response.ok) throw new Error('Failed to list profiles');
    return response.json();
  }

  async deleteVoiceProfile(profileId) {
    const response = await fetch(
      `${this.baseURL}/api/voice-converter/profiles/${encodeURIComponent(profileId)}`,
      { method: 'DELETE' }
    );
    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: response.statusText }));
      throw new Error(err.detail || 'Failed to delete profile');
    }
    return response.json();
  }

  async convertAudio(sourceFile, targetProfileId, quality = 'balanced') {
    const form = new FormData();
    form.append('source_audio', sourceFile, sourceFile.name);
    form.append('target_profile_id', targetProfileId);
    form.append('quality', quality);
    const response = await fetch(`${this.baseURL}/api/voice-converter/convert`, {
      method: 'POST',
      body: form,
      signal: AbortSignal.timeout(180_000),
    });
    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: response.statusText }));
      throw new Error(err.detail || 'Conversion failed');
    }
    return response.blob();
  }

  async convertWithNewVoice(sourceFile, refFile, quality = 'balanced') {
    const form = new FormData();
    form.append('source_audio', sourceFile, sourceFile.name);
    form.append('target_reference_audio', refFile, refFile.name);
    form.append('quality', quality);
    const response = await fetch(`${this.baseURL}/api/voice-converter/convert-with-new-voice`, {
      method: 'POST',
      body: form,
      signal: AbortSignal.timeout(180_000),
    });
    if (!response.ok) {
      const err = await response.json().catch(() => ({ detail: response.statusText }));
      throw new Error(err.detail || 'Conversion failed');
    }
    return response.blob();
  }
}

// Create and export singleton instance
const apiClient = new UnifiedAPIClient();

export default UnifiedAPIClient;
export { apiClient };
