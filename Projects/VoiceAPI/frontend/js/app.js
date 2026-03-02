/**
 * VoiceAPI Main Application
 * Handles UI interactions and orchestrates TTS synthesis
 */

import CONFIG from './config.js';
import { apiClient } from './api.js';

/**
 * Main application class
 */
class VoiceAPIApp {
  constructor() {
    // Application state
    this.languages = [];
    this.currentAudioURL = null;
    this.currentAudioMime = 'audio/wav'; // track format for download
    this.isGenerating = false;
    
    // DOM element references (cached for performance)
    this.elements = {};
  }
  
  /**
   * Initialize the application
   */
  async init() {
    console.log('🎙️ VoiceAPI Application initializing...');
    
    try {
      // 1. Cache DOM elements
      this.cacheElements();
      
      // 2. Setup event listeners
      this.setupEventListeners();
      
      // 3. Load initial data from backend
      await this.loadInitialData();
      
      // 4. Check backend health
      await this.checkBackendHealth();
      
      // 5. Initialize UI state
      this.initializeUIState();
      
      console.log('✅ VoiceAPI Application ready!');
      this.showSuccess('Connected to VoiceAPI!');
    } catch (error) {
      console.error('Initialization error:', error);
      this.showError('Failed to initialize application. Please refresh the page.');
    }
  }
  
  /**
   * Cache all DOM element references
   */
  cacheElements() {
    const elementIds = [
      'language-select',
      'text-input',
      'char-counter',
      'pace-slider',
      'pace-value',
      'pitch-slider',
      'pitch-value',
      'preprocessing-toggle',
      'generate-btn',
      'loading',
      'audio-player',
      'download-btn',
      'output-section',
      'error-container',
      'error-message',
      'success-container',
      'success-message',
      'health-voiceapi',
      'sample-btn'
    ];
    
    elementIds.forEach(id => {
      const element = document.querySelector(`[data-element="${id}"]`);
      if (element) {
        this.elements[id] = element;
      }
    });
  }
  
  /**
   * Setup all event listeners
   */
  setupEventListeners() {
    // Language selector
    this.elements['language-select']?.addEventListener('change', (e) => {
      this.handleLanguageChange(e.target.value);
    });
    
    // Text input
    this.elements['text-input']?.addEventListener('input', () => {
      this.updateCharacterCount();
    });
    
    // Pace slider
    this.elements['pace-slider']?.addEventListener('input', (e) => {
      this.updatePaceDisplay(e.target.value);
    });
    
    // Pitch slider
    this.elements['pitch-slider']?.addEventListener('input', (e) => {
      this.updatePitchDisplay(e.target.value);
    });
    
    // Generate button
    this.elements['generate-btn']?.addEventListener('click', () => {
      this.handleGenerate();
    });
    
    // Download button
    this.elements['download-btn']?.addEventListener('click', () => {
      this.handleDownload();
    });
    
    // Sample text button
    this.elements['sample-btn']?.addEventListener('click', () => {
      this.loadSampleText();
    });
    
    // Enter key in text input
    this.elements['text-input']?.addEventListener('keydown', (e) => {
      if (e.ctrlKey && e.key === 'Enter') {
        this.handleGenerate();
      }
    });
  }
  
  /**
   * Load initial data from backend
   */
  async loadInitialData() {
    try {
      this.languages = await apiClient.fetchLanguages();
      this.populateLanguageSelect();
    } catch (error) {
      console.error('Failed to load initial data:', error);
      throw error;
    }
  }
  
  /**
   * Check backend health status
   */
  async checkBackendHealth() {
    try {
      const health = await apiClient.checkHealth();
      if (this.elements['health-voiceapi']) {
        const ok = health.voiceapi_available || health.sarvam_available;
        this.elements['health-voiceapi'].className =
          ok ? 'status-indicator online' : 'status-indicator offline';
        this.elements['health-voiceapi'].title =
          ok ? 'API Online' : 'API Offline';
      }
    } catch (error) {
      console.error('Health check failed:', error);
    }
  }
  
  /**
   * Initialize UI state
   */
  initializeUIState() {
    if (this.elements['pace-slider']) {
      this.elements['pace-slider'].value = CONFIG.DEFAULTS.pace;
      this.updatePaceDisplay(CONFIG.DEFAULTS.pace);
    }
    if (this.elements['pitch-slider']) {
      this.elements['pitch-slider'].value = CONFIG.DEFAULTS.pitch;
      this.updatePitchDisplay(CONFIG.DEFAULTS.pitch);
    }
    this.updateCharacterCount();
  }
  
  /**
   * Populate language selector
   */
  populateLanguageSelect() {
    const select = this.elements['language-select'];
    if (!select) return;
    
    select.innerHTML = '';
    
    this.languages.forEach(lang => {
      const option = document.createElement('option');
      option.value = lang.code;
      option.textContent = lang.name;
      select.appendChild(option);
    });
    
    if (this.languages.length > 0) {
      select.value = this.languages[0].code;
      this.handleLanguageChange(this.languages[0].code);
    }
  }
  
  populateSpeakerSelect() {}
  
  switchProvider(provider) {}
  
  /**
   * Handle language change
   */
  handleLanguageChange(languageCode) {
    // Load sample text if available
    const sample = CONFIG.SAMPLE_TEXTS[languageCode];
    if (sample && this.elements['text-input']) {
      this.elements['text-input'].placeholder = sample;
    }
    
    // Validate language support
    this.validateLanguageSupport();
  }
  
  /**
   * Load sample text for current language
   */
  loadSampleText() {
    const languageCode = this.elements['language-select']?.value;
    const sample = CONFIG.SAMPLE_TEXTS[languageCode];
    
    if (sample && this.elements['text-input']) {
      this.elements['text-input'].value = sample;
      this.updateCharacterCount();
      this.showSuccess('Sample text loaded!');
    }
  }
  
  /**
   * Validate if current language is supported by selected provider
   */
  validateLanguageSupport() {
    this.hideError();
    if (this.elements['generate-btn'] && !this.isGenerating) {
      this.elements['generate-btn'].disabled = false;
    }
  }
  
  /**
   * Update character counter
   */
  updateCharacterCount() {
    const text = this.elements['text-input']?.value || '';
    const count = text.length;
    const counter = this.elements['char-counter'];
    
    if (!counter) return;
    
    counter.textContent = `${count} / ${CONFIG.MAX_TEXT_LENGTH}`;
    
    // Color coding
    if (count === 0) {
      counter.className = 'char-counter';
    } else if (count > CONFIG.MAX_TEXT_LENGTH) {
      counter.className = 'char-counter error';
      if (this.elements['generate-btn']) {
        this.elements['generate-btn'].disabled = true;
      }
    } else if (count > 2000) {
      counter.className = 'char-counter warning';
      if (this.elements['generate-btn'] && !this.isGenerating) {
        this.elements['generate-btn'].disabled = false;
      }
    } else {
      counter.className = 'char-counter success';
      if (this.elements['generate-btn'] && !this.isGenerating) {
        this.elements['generate-btn'].disabled = false;
      }
    }
  }
  
  /**
   * Update pace display
   */
  updatePaceDisplay(value) {
    if (this.elements['pace-value']) {
      this.elements['pace-value'].textContent = `${parseFloat(value).toFixed(1)}x`;
    }
  }
  
  /**
   * Update pitch display
   */
  updatePitchDisplay(value) {
    if (this.elements['pitch-value']) {
      const pitchValue = parseInt(value);
      const sign = pitchValue > 0 ? '+' : '';
      this.elements['pitch-value'].textContent = `${sign}${pitchValue}`;
    }
  }
  
  /**
   * Handle generate speech button click
   */
  async handleGenerate() {
    const text = this.elements['text-input']?.value?.trim();
    const language = this.elements['language-select']?.value;
    
    if (!text) {
      this.showError('Please enter some text to synthesize.');
      return;
    }
    
    if (this.isGenerating) {
      return; // Prevent multiple simultaneous generations
    }
    
    try {
      this.setLoading(true);
      this.hideError();
      this.hideSuccess();
      this.hideOutput();
      
      // Prepare synthesis parameters
      const params = {
        text: text,
        language: language,
        provider: 'auto',
        pace: parseFloat(this.elements['pace-slider']?.value || CONFIG.DEFAULTS.pace),
        pitch: parseInt(this.elements['pitch-slider']?.value || CONFIG.DEFAULTS.pitch),
        enable_preprocessing: this.elements['preprocessing-toggle']?.checked !== false
      };
      
      console.log('Generating speech:', params);
      
      // Call backend API
      const audioBlob = await apiClient.synthesize(params);
      
      // Create object URL for audio
      if (this.currentAudioURL) {
        URL.revokeObjectURL(this.currentAudioURL);
      }
      this.currentAudioMime = audioBlob.type || 'audio/wav';
      this.currentAudioURL = URL.createObjectURL(audioBlob);
      
      // Update audio player
      if (this.elements['audio-player']) {
        this.elements['audio-player'].src = this.currentAudioURL;
      }
      
      // Show output section
      this.showOutput();
      
      // Try to auto-play (may be blocked by browser)
      try {
        await this.elements['audio-player']?.play();
      } catch (playError) {
        console.log('Auto-play prevented by browser policy');
      }
      
      this.showSuccess('Speech generated successfully!');
    } catch (error) {
      console.error('Generation error:', error);
      this.showError(error.message || 'Failed to generate speech. Please try again.');
    } finally {
      this.setLoading(false);
    }
  }
  
  /**
   * Handle download button click
   */
  handleDownload() {
    if (!this.currentAudioURL) {
      this.showError('No audio to download. Please generate speech first.');
      return;
    }
    
    const a = document.createElement('a');
    a.href = this.currentAudioURL;
    
    // Use MIME type to determine file extension
    const ext = this.currentAudioMime === 'audio/mp3' || this.currentAudioMime === 'audio/mpeg' ? 'mp3' : 'wav';
    const language = this.elements['language-select']?.value || 'speech';
    const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, -5);
    
    a.download = `${language}_${timestamp}.${ext}`;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    
    this.showSuccess('Audio downloaded!');
  }
  
  /**
   * Set loading state
   */
  setLoading(isLoading) {
    this.isGenerating = isLoading;
    
    if (isLoading) {
      if (this.elements['loading']) {
        this.elements['loading'].style.display = 'flex';
      }
      if (this.elements['generate-btn']) {
        this.elements['generate-btn'].disabled = true;
        this.elements['generate-btn'].innerHTML = '⏳ Generating...';
      }
    } else {
      if (this.elements['loading']) {
        this.elements['loading'].style.display = 'none';
      }
      if (this.elements['generate-btn']) {
        this.elements['generate-btn'].disabled = false;
        this.elements['generate-btn'].innerHTML = '🎤 Generate Speech';
      }
      this.validateLanguageSupport(); // Re-validate after loading
    }
  }
  
  /**
   * Show output section
   */
  showOutput() {
    if (this.elements['output-section']) {
      this.elements['output-section'].style.display = 'block';
      this.elements['output-section'].scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  }
  
  /**
   * Hide output section
   */
  hideOutput() {
    if (this.elements['output-section']) {
      this.elements['output-section'].style.display = 'none';
    }
  }
  
  /**
   * Show error message
   */
  showError(message) {
    if (this.elements['error-message']) {
      this.elements['error-message'].textContent = message;
    }
    if (this.elements['error-container']) {
      this.elements['error-container'].style.display = 'block';
      
      // Auto-hide after configured duration
      setTimeout(() => this.hideError(), CONFIG.ERROR_DISPLAY_DURATION);
    }
  }
  
  /**
   * Hide error message
   */
  hideError() {
    if (this.elements['error-container']) {
      this.elements['error-container'].style.display = 'none';
    }
  }
  
  /**
   * Show success message
   */
  showSuccess(message) {
    if (this.elements['success-message']) {
      this.elements['success-message'].textContent = message;
    }
    if (this.elements['success-container']) {
      this.elements['success-container'].style.display = 'block';
      
      // Auto-hide after configured duration
      setTimeout(() => this.hideSuccess(), CONFIG.SUCCESS_MESSAGE_DURATION);
    }
  }
  
  /**
   * Hide success message
   */
  hideSuccess() {
    if (this.elements['success-container']) {
      this.elements['success-container'].style.display = 'none';
    }
  }
  
  /**
   * Cleanup resources
   */
  destroy() {
    // Revoke object URLs
    if (this.currentAudioURL) {
      URL.revokeObjectURL(this.currentAudioURL);
      this.currentAudioURL = null;
    }
  }
}

// Initialize application on DOM ready
document.addEventListener('DOMContentLoaded', async () => {
  const app = new VoiceAPIApp();
  await app.init();
  
  // Store app instance globally for debugging
  window.voiceAPIApp = app;
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
  if (window.voiceAPIApp) {
    window.voiceAPIApp.destroy();
  }
});

export default VoiceAPIApp;
