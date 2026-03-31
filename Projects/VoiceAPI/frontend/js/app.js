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
    this.currentAudioBlob = null;  // kept for TTS→voice-convert
    this.currentAudioMime = 'audio/wav'; // track format for download
    this.isGenerating = false;
    this._ttsVcConverting = false;
    this._ttsVcConvertedURL = null;
    
    // DOM element references (cached for performance)
    this.elements = {};
  }
  
  /**
   * Initialize the application
   */
  async init() {
    console.log('VoiceAPI Application initializing...');
    
    try {
      // 1. Cache DOM elements
      this.cacheElements();

      // 1.5 Initialize theme
      this.initializeTheme();
      
      // 2. Setup event listeners
      this.setupEventListeners();
      
      // 3. Load initial data from backend
      await this.loadInitialData();
      
      // 4. Check backend health
      await this.checkBackendHealth();
      
      // 5. Initialize UI state
      this.initializeUIState();
      
      console.log('VoiceAPI Application ready!');
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
      'sample-btn',
      'theme-toggle'
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
      this._updateSliderFill(e.target);
    });
    
    // Pitch slider
    this.elements['pitch-slider']?.addEventListener('input', (e) => {
      this.updatePitchDisplay(e.target.value);
      this._updateSliderFill(e.target);
    });
    
    // Generate button
    this.elements['generate-btn']?.addEventListener('click', () => {
      this.handleGenerate();
    });
    
    // Download button
    this.elements['download-btn']?.addEventListener('click', () => {
      this.handleDownload();
    });

    // Theme toggle
    this.elements['theme-toggle']?.addEventListener('click', () => {
      this.toggleTheme();
    });

    // TTS → Convert to My Voice
    document.getElementById('ttsVcRefreshBtn')?.addEventListener('click', () => this._loadTtsVcProfiles());
    document.getElementById('ttsVcProfileSelect')?.addEventListener('change', () => this._updateTtsVcBtn());
    document.getElementById('ttsVcConvertBtn')?.addEventListener('click', () => this._handleTtsVoiceConvert());
    document.getElementById('ttsVcDownloadBtn')?.addEventListener('click', () => {
      if (!this._ttsVcConvertedURL) return;
      const a = document.createElement('a');
      a.href = this._ttsVcConvertedURL;
      a.download = 'converted_voice.wav';
      document.body.appendChild(a); a.click(); document.body.removeChild(a);
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

  initializeTheme() {
    const storedTheme = localStorage.getItem('voiceapi-theme');
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const theme = storedTheme || (prefersDark ? 'dark' : 'light');
    this.applyTheme(theme, false);
  }

  applyTheme(theme, persist = true) {
    document.documentElement.setAttribute('data-theme', theme);
    if (persist) {
      localStorage.setItem('voiceapi-theme', theme);
    }
    if (this.elements['theme-toggle']) {
      this.elements['theme-toggle'].textContent = theme === 'dark' ? 'Light Mode' : 'Dark Mode';
    }
  }

  toggleTheme() {
    const current = document.documentElement.getAttribute('data-theme') || 'light';
    const next = current === 'dark' ? 'light' : 'dark';
    this.applyTheme(next, true);
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
      this._updateSliderFill(this.elements['pace-slider']);
    }
    if (this.elements['pitch-slider']) {
      this.elements['pitch-slider'].value = CONFIG.DEFAULTS.pitch;
      this.updatePitchDisplay(CONFIG.DEFAULTS.pitch);
      this._updateSliderFill(this.elements['pitch-slider']);
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
   * Update WebKit slider filled-track gradient so the left portion
   * of the track shows as --color-primary.
   */
  _updateSliderFill(slider) {
    const min = parseFloat(slider.min);
    const max = parseFloat(slider.max);
    const val = parseFloat(slider.value);
    const pct = ((val - min) / (max - min)) * 100;
    const primary = getComputedStyle(document.documentElement)
      .getPropertyValue('--color-primary').trim() || '#0891b2';
    const border  = getComputedStyle(document.documentElement)
      .getPropertyValue('--color-border').trim()  || '#e2e8f0';
    // Works on WebKit (Chrome/Safari) via gradient on the runnable-track background.
    // Firefox gets the filled portion from -moz-range-progress natively.
    slider.style.setProperty(
      '--slider-fill',
      `linear-gradient(to right, ${primary} ${pct}%, ${border} ${pct}%)`
    );
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
      this.currentAudioBlob = audioBlob;
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

      // Refresh TTS-VC panel: hide old result, reload profiles
      const ttsVcResult = document.getElementById('ttsVcResult');
      if (ttsVcResult) ttsVcResult.style.display = 'none';
      await this._loadTtsVcProfiles();

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
  // ── TTS → Convert to My Voice helpers ──────────────────────────────────

  async _loadTtsVcProfiles() {
    const sel = document.getElementById('ttsVcProfileSelect');
    if (!sel) return;
    try {
      const data = await apiClient.listVoiceProfiles();
      const profiles = data?.profiles || [];
      sel.innerHTML = '<option value="">Select a profile</option>';
      profiles.forEach(p => {
        const opt = document.createElement('option');
        opt.value = p.id;
        opt.textContent = p.name || p.id;
        sel.appendChild(opt);
      });
    } catch (e) {
      console.warn('Could not load voice profiles for TTS-VC panel:', e);
    }
    this._updateTtsVcBtn();
  }

  _updateTtsVcBtn() {
    const btn = document.getElementById('ttsVcConvertBtn');
    const profileId = document.getElementById('ttsVcProfileSelect')?.value;
    if (btn) btn.disabled = !profileId || !this.currentAudioBlob;
  }

  async _handleTtsVoiceConvert() {
    if (this._ttsVcConverting) return;
    const profileId = document.getElementById('ttsVcProfileSelect')?.value;
    if (!profileId || !this.currentAudioBlob) return;

    const quality = document.querySelector('input[name="ttsVcQuality"]:checked')?.value || 'balanced';
    const loading = document.getElementById('ttsVcLoading');
    const result  = document.getElementById('ttsVcResult');
    const btn     = document.getElementById('ttsVcConvertBtn');

    try {
      this._ttsVcConverting = true;
      btn.disabled = true;
      btn.textContent = 'Converting...';
      if (loading) loading.style.display = 'flex';
      if (result)  result.style.display  = 'none';

      // Build a File from the blob so the API client can name it
      const ext = this.currentAudioMime === 'audio/mp3' || this.currentAudioMime === 'audio/mpeg' ? 'mp3' : 'wav';
      const sourceFile = new File([this.currentAudioBlob], `tts_output.${ext}`, { type: this.currentAudioBlob.type });

      const convertedBlob = await apiClient.convertAudio(sourceFile, profileId, quality);

      if (this._ttsVcConvertedURL) URL.revokeObjectURL(this._ttsVcConvertedURL);
      this._ttsVcConvertedURL = URL.createObjectURL(convertedBlob);

      const player = document.getElementById('ttsVcResultPlayer');
      if (player) {
        player.src = this._ttsVcConvertedURL;
        player.load();
        try { await player.play(); } catch (_) {}
      }
      if (result) result.style.display = 'block';
    } catch (err) {
      console.error('TTS voice convert error:', err);
      this.showError(err.message || 'Voice conversion failed. Check the converter service.');
    } finally {
      this._ttsVcConverting = false;
      btn.disabled = false;
      btn.textContent = 'Convert to My Voice';
      if (loading) loading.style.display = 'none';
    }
  }

  // ── End TTS-VC helpers ────────────────────────────────────────────────────

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
        this.elements['generate-btn'].innerHTML = 'Generating...';
      }
    } else {
      if (this.elements['loading']) {
        this.elements['loading'].style.display = 'none';
      }
      if (this.elements['generate-btn']) {
        this.elements['generate-btn'].disabled = false;
        this.elements['generate-btn'].innerHTML = 'Generate Speech';
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

// =============================================================================
// Voice Converter App
// =============================================================================
class VoiceConverterApp {
  constructor() {
    this._convertedBlob = null;
    this._currentProfileId = null;
  }

  async init() {
    this._bindToggle();
    this._bindTabs();
    this._bindDropZone('vcRefDropZone', 'vcRefFileInput', 'vcRefPreview', 'vcRefPlayer', () => {
      document.getElementById('vcSaveProfileBtn').disabled =
        !document.getElementById('vcRefFileInput').files.length;
    });
    this._bindDropZone('vcSrcDropZone', 'vcSrcFileInput', 'vcSrcPreview', 'vcSrcPlayer', () => {
      this._updateConvertBtn();
    });
    document.getElementById('vcProfileSelect').addEventListener('change', () => this._updateConvertBtn());
    document.getElementById('vcSaveProfileBtn').addEventListener('click', () => this._handleSaveProfile());
    document.getElementById('vcConvertBtn').addEventListener('click', () => this._handleConvert());
    document.getElementById('vcDownloadBtn')?.addEventListener('click', () => this._handleDownload());
    document.getElementById('vcRefreshProfilesBtn').addEventListener('click', (e) => {
      e.preventDefault();
      this._loadProfiles();
    });
    // quality badges visual feedback
    document.querySelectorAll('input[name="vcQuality"]').forEach(radio => {
      radio.addEventListener('change', () => {
        document.querySelectorAll('.vc-quality-badge').forEach(b => b.classList.remove('active'));
        if (radio.checked) radio.nextElementSibling.classList.add('active');
      });
    });
    await this._checkHealth();
    await this._loadProfiles();
  }

  _bindToggle() {
    const header = document.getElementById('vcToggleHeader');
    const body   = document.getElementById('vcBody');
    const btn    = document.getElementById('vcToggleBtn');
    header.addEventListener('click', () => {
      const open = body.style.display !== 'none';
      body.style.display = open ? 'none' : 'block';
      btn.textContent = open ? 'Expand' : 'Collapse';
      btn.setAttribute('aria-expanded', String(!open));
    });
  }

  _bindTabs() {
    document.querySelectorAll('.vc-tab').forEach(tab => {
      tab.addEventListener('click', () => {
        document.querySelectorAll('.vc-tab').forEach(t => {
          t.classList.remove('active');
          t.setAttribute('aria-selected', 'false');
        });
        document.querySelectorAll('.vc-panel').forEach(p => p.style.display = 'none');
        tab.classList.add('active');
        tab.setAttribute('aria-selected', 'true');
        const panelId = 'vcPanel-' + tab.dataset.vcTab;
        const panel = document.getElementById(panelId);
        if (panel) panel.style.display = 'block';
      });
    });
  }

  _bindDropZone(zoneId, inputId, previewId, playerId, onChange) {
    const zone  = document.getElementById(zoneId);
    const input = document.getElementById(inputId);
    const preview = document.getElementById(previewId);
    const player  = document.getElementById(playerId);

    const showPreview = (file) => {
      if (!file || !file.type.startsWith('audio/')) return;
      const url = URL.createObjectURL(file);
      player.src = url;
      preview.style.display = 'block';
      zone.classList.add('has-file');
      zone.querySelector('p').textContent = file.name;
      if (onChange) onChange(file);
    };

    zone.addEventListener('click', (e) => {
      if (e.target !== input) input.click();
    });
    zone.addEventListener('keydown', (e) => {
      if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); input.click(); }
    });
    zone.addEventListener('dragover', (e) => { e.preventDefault(); zone.classList.add('drag-over'); });
    zone.addEventListener('dragleave', () => zone.classList.remove('drag-over'));
    zone.addEventListener('drop', (e) => {
      e.preventDefault();
      zone.classList.remove('drag-over');
      const file = e.dataTransfer.files[0];
      if (file) { input.files = e.dataTransfer.files; showPreview(file); }
    });
    input.addEventListener('change', () => showPreview(input.files[0]));
  }

  _updateConvertBtn() {
    const hasSrc  = document.getElementById('vcSrcFileInput').files.length > 0;
    const hasProf = document.getElementById('vcProfileSelect').value !== '';
    document.getElementById('vcConvertBtn').disabled = !(hasSrc && hasProf);
  }

  async _checkHealth() {
    const dot   = document.getElementById('vcHealthDot');
    const label = document.getElementById('vcHealthLabel');
    try {
      const data = await apiClient.converterHealth();
      const ok   = data?.status === 'healthy' || data?.status === 'ok';
      dot.className   = `status-indicator ${ok ? 'online' : 'offline'}`;
      label.textContent = ok ? 'Converter: online' : 'Converter: degraded';
    } catch {
      dot.className   = 'status-indicator offline';
      label.textContent = 'Converter: offline';
    }
  }

  async _loadProfiles() {
    try {
      const data = await apiClient.listVoiceProfiles();
      const profiles = data?.profiles || [];
      this._renderProfileSelect(profiles);
      this._renderProfileCards(profiles);
    } catch {
      // silently skip — converter may be offline
    }
  }

  _renderProfileSelect(profiles) {
    const sel = document.getElementById('vcProfileSelect');
    sel.innerHTML = '<option value="">Select saved profile</option>';
    profiles.forEach(p => {
      const opt = document.createElement('option');
      opt.value = p.id;                          // API returns 'id', not 'profile_id'
      opt.textContent = p.name || p.id;
      sel.appendChild(opt);
    });
  }

  _renderProfileCards(profiles) {
    const grid = document.getElementById('vcProfilesList');
    if (!profiles.length) {
      grid.innerHTML = '<p class="form-hint">No profiles yet. Create one in the "Create Voice Profile" tab.</p>';
      return;
    }
    grid.innerHTML = '';
    profiles.forEach(p => {
      const card = document.createElement('div');
      card.className = 'vc-profile-card';
      const date = p.created_at ? new Date(p.created_at).toLocaleDateString() : '—';
      card.innerHTML = `
        <h5>${this._escapeHtml(p.name || p.id)}</h5>
        <p>Created: ${date}</p>
        <p style="font-size:0.75rem;margin-top:0.25rem;word-break:break-all;color:var(--color-text-secondary);">${p.id}</p>
        <button class="vc-delete-btn" title="Delete profile" data-pid="${this._escapeHtml(p.id)}">Delete</button>
      `;
      card.querySelector('.vc-delete-btn').addEventListener('click', async (e) => {
        e.preventDefault();
        e.stopPropagation();
        if (!confirm(`Delete profile "${p.name || p.id}"?`)) return;
        try {
          await apiClient.deleteVoiceProfile(p.id);
          this._showSuccess('Profile deleted.');
          await this._loadProfiles();
        } catch (err) {
          this._showError(err.message);
        }
      });
      grid.appendChild(card);
    });
  }

  async _handleSaveProfile() {
    const file = document.getElementById('vcRefFileInput').files[0];
    const name = document.getElementById('vcProfileNameInput').value.trim() || 'My Voice';
    if (!file) { this._showError('Please select a reference audio file.'); return; }

    const btn = document.getElementById('vcSaveProfileBtn');
    btn.disabled = true;
    btn.textContent = 'Saving...';
    this._clearAlerts();

    try {
      const result = await apiClient.createVoiceProfile(file, name);
      this._showSuccess(`Profile "${result.profile_name || name}" saved!`);
      this._showCharacteristics(result.characteristics || result);
      await this._loadProfiles();
    } catch (err) {
      this._showError(err.message);
    } finally {
      btn.disabled = false;
      btn.textContent = 'Save Voice Profile';
    }
  }

  _showCharacteristics(chars) {
    const box = document.getElementById('vcCharacteristics');
    if (!chars) return;
    box.style.display = 'block';
    const set = (id, val, unit = '') => {
      const el = document.getElementById(id);
      if (!el) return;
      el.textContent = val != null && val !== 0
        ? `${Number(val).toFixed(1)} ${unit}`.trim()
        : '—';
    };
    // API returns flat keys: pitch_mean_hz, formant_f1_hz, speaking_rate_sps, hnr_db, duration_sec
    set('vcCharPitch', chars.pitch_mean_hz,      'Hz');
    set('vcCharRate',  chars.speaking_rate_sps,  'syl/s');
    set('vcCharF1',    chars.formant_f1_hz,       'Hz');
    set('vcCharF2',    chars.formant_f2_hz,       'Hz');
    set('vcCharHNR',   chars.hnr_db,             'dB');
    set('vcCharDur',   chars.duration_sec,        's');
  }

  async _handleConvert() {
    const srcFile  = document.getElementById('vcSrcFileInput').files[0];
    const profId   = document.getElementById('vcProfileSelect').value;
    const quality  = document.querySelector('input[name="vcQuality"]:checked')?.value || 'balanced';
    if (!srcFile || !profId) return;

    const btn = document.getElementById('vcConvertBtn');
    btn.disabled = true;
    btn.textContent = 'Converting...';
    this._clearAlerts();
    this._showProgress(10, 'Uploading audio…');

    try {
      this._showProgress(40, 'Analysing voice characteristics…');
      const blob = await apiClient.convertAudio(srcFile, profId, quality);
      this._showProgress(100, 'Done!');
      this._convertedBlob = blob;
      this._showComparison(srcFile, blob);
      this._showSuccess('Voice conversion complete.');
    } catch (err) {
      this._showError(err.message);
      this._hideProgress();
    } finally {
      btn.disabled = false;
      btn.textContent = 'Convert Voice';
    }
  }

  _showComparison(srcFile, convertedBlob) {
    const orig = document.getElementById('vcCmpOriginal');
    const conv = document.getElementById('vcCmpConverted');
    orig.src = URL.createObjectURL(srcFile);
    conv.src = URL.createObjectURL(convertedBlob);
    document.getElementById('vcComparison').style.display = 'block';
    setTimeout(() => this._hideProgress(), 600);
  }

  _handleDownload() {
    if (!this._convertedBlob) return;
    const a = document.createElement('a');
    a.href = URL.createObjectURL(this._convertedBlob);
    a.download = 'converted_voice.wav';
    a.click();
    URL.revokeObjectURL(a.href);
  }

  _showProgress(pct, label) {
    const prog  = document.getElementById('vcProgress');
    const bar   = document.getElementById('vcProgressBar');
    const lbl   = document.getElementById('vcProgressLabel');
    prog.style.display = 'block';
    bar.style.width = `${pct}%`;
    bar.setAttribute('aria-valuenow', pct);
    if (lbl) lbl.textContent = label || '';
  }

  _hideProgress() {
    const prog = document.getElementById('vcProgress');
    if (prog) prog.style.display = 'none';
  }

  _showError(msg) {
    const el = document.getElementById('vcAlertError');
    document.getElementById('vcAlertErrorMsg').textContent = msg;
    el.style.display = 'flex';
    document.getElementById('vcAlertSuccess').style.display = 'none';
    setTimeout(() => { el.style.display = 'none'; }, 8000);
  }

  _showSuccess(msg) {
    const el = document.getElementById('vcAlertSuccess');
    document.getElementById('vcAlertSuccessMsg').textContent = msg;
    el.style.display = 'flex';
    document.getElementById('vcAlertError').style.display = 'none';
    setTimeout(() => { el.style.display = 'none'; }, 5000);
  }

  _clearAlerts() {
    document.getElementById('vcAlertError').style.display = 'none';
    document.getElementById('vcAlertSuccess').style.display = 'none';
  }

  _escapeHtml(str) {
    return String(str)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;')
      .replace(/>/g, '&gt;').replace(/"/g, '&quot;')
      .replace(/'/g, '&#039;');
  }
}

// Initialize application on DOM ready
document.addEventListener('DOMContentLoaded', async () => {
  const app = new VoiceAPIApp();
  await app.init();
  
  // Store app instance globally for debugging
  window.voiceAPIApp = app;

  const vcApp = new VoiceConverterApp();
  await vcApp.init();
  window.voiceConverterApp = vcApp;
});

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
  if (window.voiceAPIApp) {
    window.voiceAPIApp.destroy();
  }
});

export default VoiceAPIApp;
