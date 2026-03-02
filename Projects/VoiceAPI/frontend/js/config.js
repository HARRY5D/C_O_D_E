/**
 * Configuration for VoiceAPI Frontend
 * All API calls go through the backend - no API keys exposed here!
 */

// ---- Resolve backend URL automatically ----
// Cases:
//   1. file:// or localhost → backend at localhost:8001
//   2. devtunnels.ms        → same tunnel-id but port 8001
//                             e.g. xxxxx-5500.devtunnels.ms → xxxxx-8001.devtunnels.ms
//   3. Any other host       → update BACKEND_TUNNEL_URL below manually
const BACKEND_TUNNEL_URL = 'https://REPLACE_WITH_YOUR_8001_TUNNEL_URL'; // fallback only

function resolveBackendURL() {
  const { hostname, protocol } = window.location;
  // Local or file:// access
  if (!hostname || hostname === 'localhost' || hostname === '127.0.0.1') {
    return 'http://localhost:8001';
  }
  // Dev Tunnels: hostname is like  abc123xyz-5500.inc1.devtunnels.ms
  // Replace the frontend port segment with 8001
  if (hostname.includes('devtunnels.ms')) {
    return protocol + '//' + hostname.replace(/-\d+\./, '-8001.');
  }
  // Any other public host (custom domain, ngrok, etc.)
  return BACKEND_TUNNEL_URL;
}

const CONFIG = {
  API_BASE_URL: resolveBackendURL(),
  
  // Text input limits
  MAX_TEXT_LENGTH: 2500,
  MIN_TEXT_LENGTH: 1,
  
  // UI Settings
  API_TIMEOUT: 60000, // 60 seconds
  ERROR_DISPLAY_DURATION: 5000, // 5 seconds
  SUCCESS_MESSAGE_DURATION: 3000, // 3 seconds
  
  // Sample texts for different languages (for testing)
  SAMPLE_TEXTS: {
    hindi: 'नमस्ते! यह एक परीक्षण संदेश है। आज का मौसम बहुत सुहावना है।',
    bengali: 'নমস্কার! এটি একটি পরীক্ষা বার্তা। আজকের আবহাওয়া খুব সুন্দর।',
    english: 'Hello! This is a test message. The weather is beautiful today.',
    gujarati: 'નમસ્તે! આ એક પરીક્ષણ સંદેશ છે। આજનું હવામાન ખૂબ જ સુંદર છે।',
    marathi: 'नमस्कार! हा एक चाचणी संदेश आहे। आजचे हवामान खूप छान आहे।',
    telugu: 'నమస్కారం! ఇది ఒక పరీక్ష సందేశం. నేటి వాతావరణం చాలా అందంగా ఉంది.',
    kannada: 'ನಮಸ್ಕಾರ! ಇದು ಒಂದು ಪರೀಕ್ಷೆಯ ಸಂದೇಶ. ಇಂದಿನ ಹವಾಮಾನ ತುಂಬಾ ಸುಂದರವಾಗಿದೆ.',
    tamil: 'வணக்கம்! இது ஒரு சோதனை செய்தி. இன்றைய வானிலை மிக அழகாக உள்ளது.',
    malayalam: 'നമസ്കാരം! ഇത് ഒരു ടെസ്റ്റ് സന്ദേശമാണ്. ഇന്നത്തെ കാലാവസ്ഥ വളരെ മനോഹരമാണ്.',
    punjabi: 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ! ਇਹ ਇੱਕ ਟੈਸਟ ਸੁਨੇਹਾ ਹੈ। ਅੱਜ ਦਾ ਮੌਸਮ ਬਹੁਤ ਸੁੰਦਰ ਹੈ।',
    odia: 'ନମସ୍କାର! ଏହା ଏକ ପରୀକ୍ଷା ବାର୍ତ୍ତା। ଆଜିର ପାଗ ବହୁତ ସୁନ୍ଦର।',
    bhojpuri: 'प्रणाम! ई एगो परीक्षण संदेश बा। आज के मौसम बहुत बढ़िया बा।',
    chhattisgarhi: 'नमस्कार! ये एक परीक्षण संदेश हे। आज के मौसम बहुत बढ़िया हे।',
    maithili: 'प्रणाम! ई एकटा परीक्षण संदेश अछि। आइक मौसम बहुत नीक अछि।',
    magahi: 'प्रणाम! ई एगो परीक्षण संदेश हऽ। आज के मौसम बहुत बढ़िया हऽ।'
  },
  
  // Default synthesis settings
  DEFAULTS: {
    provider: 'voiceapi',
    speaker: 'meera',
    pace: 1.0,
    pitch: 0
  },
  
  // Provider display names
  PROVIDER_NAMES: {
    voiceapi: 'Free (VITS)',
    sarvam: 'Premium (AI)'
  }
};

// Export for use in other modules
export default CONFIG;
