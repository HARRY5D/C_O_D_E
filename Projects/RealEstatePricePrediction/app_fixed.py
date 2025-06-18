#!/usr/bin/env python3
"""
Real Estate Price Prediction Web Application
Flask-based web service for predicting property prices in Ahmedabad
"""

from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd
import json
import os
from datetime import datetime
import logging
import sys

# Add src directory to path
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# Import with error handling
try:
    from real_data_processor import RealDataProcessor
    PROCESSOR_AVAILABLE = True
    print("✅ RealDataProcessor imported successfully")
except ImportError as e:
    print(f"⚠️ Warning: Could not import RealDataProcessor: {e}")
    RealDataProcessor = None
    PROCESSOR_AVAILABLE = False

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RealEstatePredictionAPI:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.model_metadata = None
        
        # Initialize processor if available
        if PROCESSOR_AVAILABLE:
            self.processor = RealDataProcessor()
        else:
            self.processor = None
            
        self.load_model_components()
    
    def load_model_components(self):
        """Load the trained model and preprocessing components"""
        try:
            models_dir = os.path.join(os.path.dirname(__file__), 'models')
            
            # Load model
            model_path = os.path.join(models_dir, 'best_model_gradient_boosting.joblib')
            if os.path.exists(model_path):
                self.model = joblib.load(model_path)
                logger.info("✅ Model loaded successfully")
            else:
                logger.error(f"❌ Model file not found: {model_path}")
                return False
            
            # Load scaler
            scaler_path = os.path.join(models_dir, 'scaler.joblib')
            if os.path.exists(scaler_path):
                self.scaler = joblib.load(scaler_path)
                logger.info("✅ Scaler loaded successfully")
            
            # Load feature columns
            feature_cols_path = os.path.join(models_dir, 'feature_columns.joblib')
            if os.path.exists(feature_cols_path):
                self.feature_columns = joblib.load(feature_cols_path)
                logger.info("✅ Feature columns loaded successfully")
            
            # Load metadata
            metadata_path = os.path.join(models_dir, 'model_metadata.json')
            if os.path.exists(metadata_path):
                with open(metadata_path, 'r') as f:
                    self.model_metadata = json.load(f)
                logger.info("✅ Model metadata loaded successfully")
                
                logger.info(f"📊 Model: {self.model_metadata.get('model_name', 'Unknown')}")
                logger.info(f"📈 R² Score: {self.model_metadata.get('r2_score', 'Unknown')}")
                logger.info(f"🔧 Features: {self.model_metadata.get('features_count', 'Unknown')}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error loading model components: {e}")
            return False
    
    def prepare_features(self, property_data):
        """Prepare features for prediction based on input data"""
        try:
            # Create a DataFrame with the input data
            df = pd.DataFrame([property_data])
            
            # Calculate Ahmedabad city center coordinates
            ahmedabad_center_lat = 23.0225
            ahmedabad_center_lon = 72.5714
            
            # Ensure we have coordinates
            lat = float(property_data.get('latitude', ahmedabad_center_lat))
            lng = float(property_data.get('longitude', ahmedabad_center_lon))
            
            # Basic features
            bedrooms = int(property_data.get('bedrooms', 2))
            bathrooms = int(property_data.get('bathrooms', 2))
            square_feet = float(property_data.get('square_feet', 1000))
            property_age = int(property_data.get('property_age', 5))
            
            # Set basic features
            df['bedrooms'] = bedrooms
            df['bathrooms'] = bathrooms
            df['square_feet'] = square_feet
            df['property_age'] = property_age
            df['latitude'] = lat
            df['longitude'] = lng
            
            # Advanced features (matching training pipeline)
            df['distance_from_center'] = np.sqrt(
                (lat - ahmedabad_center_lat)**2 + 
                (lng - ahmedabad_center_lon)**2
            )
            
            df['luxury_score'] = (
                (square_feet / 1000) * 0.3 +
                bathrooms * 0.2 +
                (bedrooms / 5) * 0.2 +
                (1 / (df['distance_from_center'].iloc[0] + 0.01)) * 0.3
            )
            
            df['price_per_sqft'] = 3000  # Default value
            df['room_density'] = (bedrooms + bathrooms) / square_feet * 1000
            
            # Location cluster (simplified)
            df['location_cluster'] = 0  # Default cluster
            
            # Interaction features
            df['bedrooms_x_bathrooms'] = bedrooms * bathrooms
            df['area_x_luxury'] = square_feet * df['luxury_score'].iloc[0]
            
            # Binned features (simplified)
            df['area_bin'] = min(9, max(0, int((square_feet - 200) / 1000)))  # 0-9 bins
            df['price_bin'] = 5  # Default bin
            
            # Additional features
            df['room_efficiency'] = bedrooms / square_feet * 1000
            df['bathroom_ratio'] = bathrooms / max(1, bedrooms)  # Avoid division by zero
            
            # If we have feature columns from training, ensure all are present
            if self.feature_columns:
                for col in self.feature_columns:
                    if col not in df.columns:
                        df[col] = 0  # Default value for missing features
                
                # Select only the features used in training and in the right order
                df_features = df[self.feature_columns]
            else:
                # Use all created features
                df_features = df
            
            # Fill any NaN values
            df_features = df_features.fillna(0)
            
            return df_features
            
        except Exception as e:
            logger.error(f"Error preparing features: {e}")
            raise
    
    def predict_price(self, property_data):
        """Predict property price based on input features"""
        try:
            if not self.model:
                raise ValueError("Model not loaded")
            
            # Prepare features
            features = self.prepare_features(property_data)
            
            # Make prediction
            prediction = self.model.predict(features)[0]
            
            # Calculate confidence intervals (approximate ±15%)
            confidence_low = prediction * 0.85
            confidence_high = prediction * 1.15
            
            return {
                'predicted_price': float(prediction),
                'confidence_low': float(confidence_low),
                'confidence_high': float(confidence_high),
                'currency': 'INR',
                'model_info': {
                    'model_name': self.model_metadata.get('model_name', 'Gradient Boosting') if self.model_metadata else 'Gradient Boosting',
                    'r2_score': self.model_metadata.get('r2_score', 'Unknown') if self.model_metadata else 'Unknown',
                    'prediction_date': datetime.now().isoformat()
                }
            }
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            raise

# Initialize the prediction API
try:
    prediction_api = RealEstatePredictionAPI()
    API_LOADED = True
except Exception as e:
    logger.error(f"Failed to initialize prediction API: {e}")
    prediction_api = None
    API_LOADED = False

@app.route('/')
def index():
    """Main page with map interface"""
    try:
        return render_template('index.html', 
                             model_loaded=API_LOADED,
                             model_info=prediction_api.model_metadata if prediction_api else None)
    except Exception as e:
        logger.error(f"Error serving index page: {e}")
        return f"Error loading page: {e}", 500

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for price prediction"""
    try:
        if not API_LOADED:
            return jsonify({
                'error': 'Prediction API not available',
                'success': False
            }), 503
        
        # Get property data from request
        if request.is_json:
            property_data = request.get_json()
        else:
            property_data = request.form.to_dict()
        
        # Convert string values to appropriate types
        for key, value in property_data.items():
            if key in ['bedrooms', 'bathrooms', 'property_age']:
                property_data[key] = int(float(value))
            elif key in ['latitude', 'longitude', 'square_feet']:
                property_data[key] = float(value)
        
        # Validate required fields
        required_fields = ['latitude', 'longitude', 'bedrooms', 'bathrooms', 'square_feet']
        for field in required_fields:
            if field not in property_data or property_data[field] is None:
                return jsonify({
                    'error': f'Missing required field: {field}',
                    'success': False
                }), 400
        
        # Make prediction
        result = prediction_api.predict_price(property_data)
        result['success'] = True
        
        logger.info(f"Prediction made: ₹{result['predicted_price']:,.0f} for property at ({property_data['latitude']:.4f}, {property_data['longitude']:.4f})")
        
        return jsonify(result)
        
    except Exception as e:
        logger.error(f"Error in prediction endpoint: {e}")
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/model-info')
def model_info():
    """Get model information"""
    try:
        if not API_LOADED:
            return jsonify({
                'error': 'Model not loaded',
                'success': False
            }), 503
            
        return jsonify({
            'model_metadata': prediction_api.model_metadata,
            'feature_count': len(prediction_api.feature_columns) if prediction_api.feature_columns else 0,
            'features': prediction_api.feature_columns if prediction_api.feature_columns else [],
            'success': True
        })
    except Exception as e:
        return jsonify({
            'error': str(e),
            'success': False
        }), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy' if API_LOADED else 'degraded',
        'model_loaded': API_LOADED,
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found', 'success': False}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error', 'success': False}), 500

if __name__ == '__main__':
    print("🚀 Starting Real Estate Price Prediction Server...")
    print(f"📁 Current directory: {os.getcwd()}")
    print(f"🤖 API Status: {'Loaded' if API_LOADED else 'Failed to load'}")
    
    if prediction_api and prediction_api.model_metadata:
        print(f"📊 Model: {prediction_api.model_metadata.get('model_name', 'Unknown')}")
        print(f"📈 Model R² Score: {prediction_api.model_metadata.get('r2_score', 'Unknown')}")
        print(f"🗓️ Training Date: {prediction_api.model_metadata.get('training_date', 'Unknown')[:19]}")
    
    print(f"🌐 Server starting at: http://localhost:5000")
    print("🗺️ Interactive map available at the main page")
    
    # Run with error handling
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        input("Press Enter to exit...")
