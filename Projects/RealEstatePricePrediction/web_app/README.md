# Real Estate Price Predictor Web Application

A sophisticated web application that uses machine learning to predict real estate prices in Ahmedabad, India. Built with Flask backend and interactive frontend featuring map-based property selection.

## 🚀 Features

- **Interactive Map Interface**: Click anywhere on the map to select property location
- **AI-Powered Predictions**: Uses trained Gradient Boosting model with 99.3% accuracy
- **Real-Time Analysis**: Instant price predictions with confidence intervals
- **Responsive Design**: Works perfectly on desktop, tablet, and mobile devices
- **Professional UI**: Modern, clean interface with smooth animations

## 📊 Model Performance

- **Accuracy**: R² Score of 0.9932 (99.3% accuracy)
- **Speed**: ~1.4ms per prediction
- **Reliability**: 99.6% of predictions within 20% accuracy range
- **Features**: 30+ property attributes for comprehensive analysis

## 🛠️ Installation

### Prerequisites

1. Python 3.8 or higher
2. All dependencies from `requirements.txt`

### Setup

1. **Navigate to the web app directory**:
   ```bash
   cd C:\Users\dipes\Desktop\JAVA\CODE\Projects\RealEstatePricePrediction\web_app
   ```

2. **Install dependencies** (if not already installed):
   ```bash
   pip install -r ../requirements.txt
   ```

3. **Ensure the trained model exists**:
   - Model file: `../models/best_model_gradient_boosting.joblib`
   - Scaler file: `../models/scaler.joblib`
   - Features file: `../models/feature_columns.joblib`
   - Metadata file: `../models/model_metadata.json`

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

## 🗂️ Project Structure

```
web_app/
├── app.py                 # Main Flask application
├── templates/
│   ├── index.html        # Main page template
│   ├── 404.html          # Error page template
│   └── 500.html          # Server error template
├── static/
│   ├── css/
│   │   └── style.css     # Custom CSS styles
│   └── js/
│       └── app.js        # Custom JavaScript
└── README.md             # This file
```

## 🎯 How to Use

### Step 1: Select Property Location
- **Interactive Map**: Click anywhere on the map to select a property location
- **Default Location**: Starts at Ahmedabad city center
- **Coordinates**: Latitude and longitude are automatically updated

### Step 2: Enter Property Details
- **Bedrooms**: Select number of bedrooms (1-5+)
- **Bathrooms**: Select number of bathrooms (1-4+)
- **Area**: Enter property area in square feet (200-10,000)
- **Property Age**: Select age category (New to 15+ years)

### Step 3: Get Prediction
- Click "Predict Property Price" button
- View instant prediction with confidence interval
- See property summary and technical details

## 🔧 Technical Details

### Backend (Flask)
- **Framework**: Flask 2.3.3
- **Model Loading**: Joblib for model persistence
- **API Endpoints**:
  - `/` - Main application page
  - `/predict` - Price prediction API
  - `/api/model-info` - Model information
  - `/health` - Health check

### Frontend
- **Map Library**: Leaflet.js for interactive maps
- **UI Framework**: Bootstrap 5.3.0
- **Icons**: Font Awesome 6.4.0
- **Responsive Design**: Mobile-first approach

### Machine Learning
- **Algorithm**: Gradient Boosting Regressor
- **Features**: 30+ engineered features including:
  - Property details (bedrooms, bathrooms, area)
  - Location features (distance from center, coordinates)
  - Derived features (luxury score, room density)
  - Statistical features (neighborhood pricing)

## 📡 API Endpoints

### POST /predict
Predict property price based on input features.

**Request Body**:
```json
{
  "bedrooms": 3,
  "bathrooms": 2,
  "square_feet": 1200,
  "latitude": 23.0225,
  "longitude": 72.5714,
  "property_age": 5
}
```

**Response**:
```json
{
  "success": true,
  "prediction": {
    "predicted_price": 5500000,
    "lower_bound": 4950000,
    "upper_bound": 6050000,
    "currency": "INR",
    "model_name": "Gradient Boosting",
    "prediction_date": "2025-06-10T19:30:00"
  },
  "input_data": { ... }
}
```

### GET /api/model-info
Get information about the loaded model.

**Response**:
```json
{
  "model_loaded": true,
  "metadata": {
    "model_name": "Gradient Boosting",
    "r2_score": 0.9932,
    "training_samples": 2556,
    "features_count": 30
  },
  "feature_count": 30
}
```

## 🔍 Features Explained

### Location-Based Features
- **Distance from Center**: Calculated distance from Ahmedabad city center
- **Location Cluster**: Machine learning-based neighborhood clustering
- **Coordinates**: Exact latitude and longitude

### Property Features
- **Basic Details**: Bedrooms, bathrooms, area, age
- **Derived Metrics**: 
  - Luxury Score: Composite score based on size and amenities
  - Room Density: Rooms per square foot
  - Room Efficiency: Bedroom utilization
  - Bathroom Ratio: Bathrooms per bedroom

### Advanced Features
- **Price per Sq Ft**: Estimated value density
- **Area Binning**: Categorical area ranges
- **Interaction Features**: Combined property attributes

## 🛡️ Error Handling

- **Model Loading**: Graceful handling of missing model files
- **Input Validation**: Client and server-side validation
- **Error Pages**: Custom 404 and 500 error pages
- **API Errors**: Structured error responses with details

## 🔧 Configuration

### Environment Variables (Optional)
```bash
FLASK_ENV=development          # Development mode
FLASK_DEBUG=True              # Enable debug mode
MODEL_PATH=../models/         # Custom model directory
```

### Security Notes
- Change the secret key in production
- Use HTTPS in production
- Implement rate limiting for API endpoints
- Add authentication for sensitive operations

## 📱 Mobile Compatibility

- **Responsive Design**: Adapts to all screen sizes
- **Touch-Friendly**: Large buttons and touch targets
- **Mobile Maps**: Optimized map controls for mobile
- **Fast Loading**: Optimized assets for mobile networks

## 🚀 Deployment

### Local Development
```bash
python app.py
```

### Production Deployment
1. **Use a production WSGI server** (e.g., Gunicorn):
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

2. **Set up reverse proxy** (nginx recommended)

3. **Use environment variables** for configuration

4. **Enable HTTPS** for secure communication

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📋 TODO / Future Enhancements

- [ ] Add property photos upload and analysis
- [ ] Implement user accounts and prediction history
- [ ] Add market trend analysis
- [ ] Include property comparison features
- [ ] Add export functionality (PDF reports)
- [ ] Implement caching for better performance
- [ ] Add API rate limiting
- [ ] Include property amenities checklist

## 🐛 Troubleshooting

### Common Issues

1. **Model not loading**:
   - Check if model files exist in `../models/` directory
   - Verify file permissions
   - Check console output for specific errors

2. **Map not displaying**:
   - Check internet connection (requires external map tiles)
   - Verify JavaScript console for errors
   - Try refreshing the page

3. **Prediction errors**:
   - Validate input ranges (area: 200-10,000 sq ft)
   - Check if all required fields are filled
   - Verify coordinates are within reasonable bounds

### Debug Mode
Run with debug enabled to see detailed error messages:
```bash
FLASK_DEBUG=True python app.py
```

## 📞 Support

For issues, questions, or contributions:
- Check the console output for detailed error messages
- Verify all dependencies are installed correctly
- Ensure the trained model files are present

## 📄 License

This project is part of the Real Estate Price Prediction Platform for educational and demonstration purposes.

---

**Built with ❤️ using Flask, Scikit-learn, and Leaflet Maps**
