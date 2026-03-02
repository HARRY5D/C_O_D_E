# 🎤 VoiceAPI - Multi-lingual Text-to-Speech Platform

A fullstack web application providing high-quality text-to-speech synthesis in 15+ Indian languages. Built with FastAPI backend and vanilla JavaScript frontend.

![VoiceAPI Banner](https://img.shields.io/badge/TTS-Multi--lingual-blue) ![License](https://img.shields.io/badge/license-MIT-green) ![Python](https://img.shields.io/badge/python-3.8+-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-0.109-teal)

## ✨ Features

- 🌏 **15+ Indian Languages** - Hindi, Bengali, Tamil, Telugu, Gujarati, Marathi, Kannada, Malayalam, Punjabi, Odia, and more
- 🎭 **35+ AI Voices** - Multiple speakers with different genders and styles
- ⚡ **Dual Providers** - Free VITS models + Premium Sarvam.ai API
- 🎛️ **Customizable** - Adjust speech pace, pitch, and preprocessing
- 🔒 **Secure** - API keys stored securely in backend (never exposed)
- 📱 **Responsive** - Works on desktop, tablet, and mobile
- 🎨 **Modern UI** - Clean, minimalist design with smooth animations

## 🏗️ Architecture

```
VoiceAPI/
├── backend/              # FastAPI Python server
│   ├── main.py          # Main application server
│   ├── voiceapi_client.py   # VITS-based TTS client
│   ├── sarvam_client.py     # Sarvam.ai API client
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables (API keys)
├── frontend/            # Vanilla JavaScript SPA
│   ├── index.html       # Main HTML page
│   ├── css/
│   │   └── styles.css   # Modern responsive styles
│   └── js/
│       ├── config.js    # Frontend configuration
│       ├── api.js       # Backend API client
│       └── app.js       # Main application logic
├── README.md           # This file
└── .gitignore          # Git ignore rules
```

### Technology Stack

**Backend:**
- **FastAPI** - Modern Python web framework
- **HTTPx** - Async HTTP client
- **Pydantic** - Data validation
- **python-dotenv** - Environment management

**Frontend:**
- **Vanilla JavaScript** - ES6 modules
- **CSS3** - Modern responsive design
- **HTML5 Audio** - Native audio playback

**TTS Providers:**
- **Your VoiceAPI** - VITS-based models (11 languages)
- **Sarvam.ai** - Neural TTS (11 languages, 35+ speakers)

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- A modern web browser
- Sarvam.ai API key (optional, for premium features)

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   
   Edit `backend/.env` and add your Sarvam API key:
   ```env
   SARVAM_API_KEY=your_actual_api_key_here
   VOICEAPI_BASE_URL=https://harshil748-voiceapi.hf.space
   CORS_ORIGINS=http://localhost:3000,http://localhost:5500
   HOST=0.0.0.0
   PORT=8001
   ```

   > **Get your Sarvam API key:** Visit [sarvam.ai](https://www.sarvam.ai/) and sign up

4. **Start the backend server:**
   ```bash
   python main.py
   ```

   The backend will be available at: `http://localhost:8001`
   
   API documentation: `http://localhost:8001/docs`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Start a local web server:**

   **Option A: Python HTTP Server**
   ```bash
   python -m http.server 3000
   ```

   **Option B: Node.js HTTP Server**
   ```bash
   npx http-server -p 3000
   ```

   **Option C: VS Code Live Server**
   - Install "Live Server" extension
   - Right-click `index.html` → "Open with Live Server"

3. **Open in browser:**
   
   Navigate to: `http://localhost:3000`

## 📖 Usage

1. **Select Language** - Choose from 15+ supported languages
2. **Choose Provider** - Free (VITS) or Premium (AI)
3. **Enter Text** - Type or paste text (max 2500 characters)
4. **Adjust Settings** - Optional: modify pace, pitch, speaker
5. **Generate** - Click "Generate Speech" or press Ctrl+Enter
6. **Download** - Save the audio file to your device

### Keyboard Shortcuts

- `Ctrl + Enter` - Generate speech
- `Tab` - Navigate between fields

## 🔧 API Documentation

### Endpoints

#### Health Check
```http
GET /api/health
```
Returns status of both TTS providers.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2026-02-20T10:30:00",
  "voiceapi_available": true,
  "sarvam_available": true
}
```

#### List Languages
```http
GET /api/languages
```
Returns all supported languages with provider availability.

**Response:**
```json
[
  {
    "code": "hindi",
    "name": "Hindi (हिन्दी)",
    "voiceapi_supported": true,
    "sarvam_supported": true,
    "sarvam_code": "hi-IN"
  }
]
```

#### List Speakers
```http
GET /api/speakers
```
Returns available AI voices (Sarvam.ai only).

**Response:**
```json
[
  {
    "id": "meera",
    "name": "Meera",
    "gender": "female",
    "language": "Hindi"
  }
]
```

#### Synthesize Speech
```http
POST /api/synthesize
Content-Type: application/json

{
  "text": "Your text here",
  "language": "hindi",
  "provider": "voiceapi",
  "speaker": "meera",
  "pace": 1.0,
  "pitch": 0,
  "enable_preprocessing": true
}
```

**Response:** Audio file (WAV for VoiceAPI, MP3 for Sarvam)

## 🌐 Deployment

### Backend Deployment (Railway)

1. **Install Railway CLI:**
   ```bash
   npm install -g @railway/cli
   ```

2. **Login and deploy:**
   ```bash
   cd backend
   railway login
   railway init
   railway up
   ```

3. **Set environment variables in Railway dashboard:**
   - `SARVAM_API_KEY` - Your Sarvam.ai API key
   - `CORS_ORIGINS` - Your frontend URL
   - `HOST` - 0.0.0.0
   - `PORT` - 8001

### Frontend Deployment (Netlify)

1. **Install Netlify CLI:**
   ```bash
   npm install -g netlify-cli
   ```

2. **Deploy:**
   ```bash
   cd frontend
   netlify deploy --prod
   ```

3. **Update API URL:**
   
   Edit `frontend/js/config.js`:
   ```javascript
   API_BASE_URL: 'https://your-backend-url.railway.app'
   ```

### Alternative Deployment Options

- **Backend:** Heroku, Render, Google Cloud Run, AWS Lambda
- **Frontend:** Vercel, GitHub Pages, Cloudflare Pages

## 🔒 Security

✅ **API Keys Protected** - Stored only in backend `.env` file  
✅ **CORS Configured** - Whitelist specific frontend origins  
✅ **Input Validation** - Backend validates all user inputs  
✅ **Rate Limiting** - Can be added via middleware  
✅ **HTTPS Ready** - Works with SSL certificates  

### Important Security Notes

1. **Never commit `.env` files** - Already in `.gitignore`
2. **Rotate API keys** if accidentally exposed
3. **Use environment variables** for all secrets
4. **Enable HTTPS** in production
5. **Update CORS origins** for production URLs

## 🛠️ Development

### Project Structure Explained

- **`backend/main.py`** - FastAPI app with all endpoints
- **`backend/voiceapi_client.py`** - Wrapper for your VITS TTS API
- **`backend/sarvam_client.py`** - Wrapper for Sarvam.ai API
- **`frontend/js/config.js`** - Frontend configuration constants
- **`frontend/js/api.js`** - Backend API communication
- **`frontend/js/app.js`** - Main UI logic and event handling

### Adding New Languages

1. Update `LANGUAGE_MAPPING` in `backend/main.py`
2. Add sample text in `frontend/js/config.js`
3. Test with both providers

### Customizing UI

Edit `frontend/css/styles.css`:
- **Colors:** Modify CSS custom properties in `:root`
- **Layout:** Adjust spacing and grid properties
- **Typography:** Change font families and sizes

## 📊 Supported Languages

| Language | VoiceAPI (Free) | Sarvam (Premium) |
|----------|----------------|------------------|
| Hindi (हिन्दी) | ✅ | ✅ |
| Bengali (বাংলা) | ✅ | ✅ |
| English | ✅ | ✅ |
| Gujarati (ગુજરાતી) | ✅ | ✅ |
| Marathi (मराठी) | ✅ | ✅ |
| Telugu (తెలుగు) | ✅ | ✅ |
| Kannada (ಕನ್ನಡ) | ✅ | ✅ |
| Tamil (தமிழ்) | ❌ | ✅ |
| Malayalam (മലയാളം) | ❌ | ✅ |
| Punjabi (ਪੰਜਾਬੀ) | ❌ | ✅ |
| Odia (ଓଡ଼ିଆ) | ❌ | ✅ |
| Bhojpuri | ✅ | ❌ |
| Chhattisgarhi | ✅ | ❌ |
| Maithili | ✅ | ❌ |
| Magahi | ✅ | ❌ |

## 🐛 Troubleshooting

### Backend won't start

**Problem:** `ModuleNotFoundError` or import errors

**Solution:**
```bash
cd backend
pip install -r requirements.txt --upgrade
```

**Problem:** Port 8001 already in use

**Solution:** Change `PORT` in `.env` or kill existing process:
```bash
# Windows
netstat -ano | findstr :8001
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:8001 | xargs kill
```

### Frontend can't connect

**Problem:** CORS errors in browser console

**Solution:** Add your frontend URL to `CORS_ORIGINS` in backend `.env`:
```env
CORS_ORIGINS=http://localhost:3000,http://localhost:5500,http://127.0.0.1:5500
```

**Problem:** "Failed to fetch" errors

**Solution:** Ensure backend is running and check `API_BASE_URL` in `frontend/js/config.js`

### Sarvam API errors

**Problem:** 401 Authentication Failed

**Solution:** Check your API key in `backend/.env`:
```env
SARVAM_API_KEY=your_correct_api_key
```

**Problem:** 429 Rate Limit Exceeded

**Solution:** Wait a moment or upgrade your Sarvam.ai plan

### Audio playback issues

**Problem:** Audio doesn't auto-play

**Solution:** Browser autoplay policies may block it. User must click play manually.

**Problem:** Downloaded audio is corrupted

**Solution:** Ensure backend returns proper audio content-type headers

## 🤝 Contributing

Contributions are welcome! Here's how:

1. **Fork the repository**
2. **Create a feature branch:** `git checkout -b feature/amazing-feature`
3. **Commit changes:** `git commit -m 'Add amazing feature'`
4. **Push to branch:** `git push origin feature/amazing-feature`
5. **Open a Pull Request**

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **FastAPI** - For the excellent Python web framework
- **Sarvam.ai** - For high-quality Indian language TTS
- **VITS** - For open-source TTS models
- **Hugging Face** - For hosting the VoiceAPI space

## 📧 Contact & Support

- **Issues:** [GitHub Issues](https://github.com/HARRY5D/C_O_D_E/issues)
- **Discussions:** [GitHub Discussions](https://github.com/HARRY5D/C_O_D_E/discussions)
- **Email:** support@voiceapi.example.com

## 🗺️ Roadmap

- [ ] Real-time streaming TTS
- [ ] Voice cloning support
- [ ] Batch processing API
- [ ] Mobile apps (iOS/Android)
- [ ] More language support
- [ ] Custom voice training
- [ ] API rate limiting
- [ ] User authentication
- [ ] Usage analytics dashboard

---

**Made with ❤️ for Indian languages**

*Last updated: February 20, 2026*
