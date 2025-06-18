#!/usr/bin/env python3
"""
Real Estate Price Prediction Web Application
Uses the trained Gradient Boosting model to predict property prices in Ahmedabad
"""

import os
import sys
import json
import joblib
import numpy as np
import pandas as pd
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from datetime import datetime
import logging

# Add the src directory to the path to import custom modules
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'src'))

try:
    from real_data_processor import RealDataProcessor
except ImportError:
    print("Warning: Could not import RealDataProcessor. Some features may not work.")
    RealDataProcessor = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Configuration
MODEL_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'models')
MODEL_PATH = os.path.join(MODEL_DIR, 'best_model_gradient_boosting.joblib')
SCALER_PATH = os.path.join(MODEL_DIR, 'scaler.joblib')
FEATURES_PATH = os.path.join(MODEL_DIR, 'feature_columns.joblib')
METADATA_PATH = os.path.join(MODEL_DIR, 'model_metadata.json')

class RealEstatePredictorApp:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.feature_columns = None
        self.metadata = None
        self.load_model_components()
    
    def load_model_components(self):
        """Load the trained model and preprocessing components"""
        try:
            # Load model
            if os.path.exists(MODEL_PATH):
                self.model = joblib.load(MODEL_PATH)
                logger.info("✅ Model loaded successfully")
            else:
                logger.error(f"❌ Model not found at {MODEL_PATH}")
                return False
            
            # Load scaler
            if os.path.exists(SCALER_PATH):
                self.scaler = joblib.load(SCALER_PATH)
                logger.info("✅ Scaler loaded successfully")
            
            # Load feature columns
            if os.path.exists(FEATURES_PATH):
                self.feature_columns = joblib.load(FEATURES_PATH)
                logger.info("✅ Feature columns loaded successfully")
            
            # Load metadata
            if os.path.exists(METADATA_PATH):
                with open(METADATA_PATH, 'r') as f:
                    self.metadata = json.load(f)
                logger.info("✅ Metadata loaded successfully")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Error loading model components: {e}")
            return False
    
    def prepare_features(self, property_data):
        """Prepare features for prediction based on user input"""
        try:
            # Create a DataFrame with the input data
            df = pd.DataFrame([property_data])
            
            # Add derived features similar to training
            ahmedabad_center_lat = 23.0225
            ahmedabad_center_lon = 72.5714
            
            # Use provided coordinates or default to city center
            lat = property_data.get('latitude', ahmedabad_center_lat)
            lon = property_data.get('longitude', ahmedabad_center_lon)
            
            # Calculate derived features
            df['distance_from_center'] = np.sqrt(
                (lat - ahmedabad_center_lat)**2 + 
                (lon - ahmedabad_center_lon)**2
            )
            
            df['luxury_score'] = (
                (df['square_feet'] / 1000) * 0.3 +
                df['bathrooms'] * 0.2 +
                (df['bedrooms'] / 5) * 0.2 +
                (1 / (df['distance_from_center'] + 0.01)) * 0.3
            )
            
            df['price_per_sqft'] = 5000  # Default estimate for calculation
            df['room_density'] = (df['bedrooms'] + df['bathrooms']) / df['square_feet'] * 1000
            df['location_cluster'] = 1  # Default cluster
            df['bedrooms_x_bathrooms'] = df['bedrooms'] * df['bathrooms']
            df['area_x_luxury'] = df['square_feet'] * df['luxury_score']
            df['area_bin'] = 5  # Default bin
            df['price_bin'] = 5  # Default bin
            df['room_efficiency'] = df['bedrooms'] / df['square_feet'] * 1000
            df['bathroom_ratio'] = df['bathrooms'] / df['bedrooms'].replace(0, 1)
            
            # Add missing columns with default values
            if self.feature_columns:
                for col in self.feature_columns:
                    if col not in df.columns:
                        df[col] = 0  # Default value for missing features
                
                # Reorder columns to match training
                df = df.reindex(columns=self.feature_columns, fill_value=0)
            
            return df.iloc[0].values.reshape(1, -1)
            
        except Exception as e:
            logger.error(f"Error preparing features: {e}")
            return None
    
    def predict_price(self, property_data):
        """Predict property price based on input features"""
        try:
            if not self.model:
                return {"error": "Model not loaded"}
            
            # Prepare features
            features = self.prepare_features(property_data)
            if features is None:
                return {"error": "Failed to prepare features"}
            
            # Make prediction
            prediction = self.model.predict(features)[0]
            
            # Calculate confidence intervals (simple approach)
            base_uncertainty = prediction * 0.1  # 10% uncertainty
            lower_bound = prediction - base_uncertainty
            upper_bound = prediction + base_uncertainty
            
            return {
                "predicted_price": float(prediction),
                "lower_bound": float(lower_bound),
                "upper_bound": float(upper_bound),
                "currency": "INR",
                "model_name": self.metadata.get('model_name', 'Gradient Boosting') if self.metadata else 'Gradient Boosting',
                "prediction_date": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            return {"error": f"Prediction failed: {str(e)}"}

# Initialize the predictor
predictor_app = RealEstatePredictorApp()

@app.route('/')
def index():
    """Main page with map interface"""
    return render_template('index.html', 
                         model_info=predictor_app.metadata,
                         model_loaded=predictor_app.model is not None)

@app.route('/predict', methods=['POST'])
def predict():
    """API endpoint for price prediction"""
    try:
        # Get data from form or JSON
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form.to_dict()
        
        # Convert string values to appropriate types
        property_data = {
            'bedrooms': int(data.get('bedrooms', 2)),
            'bathrooms': int(data.get('bathrooms', 2)),
            'square_feet': float(data.get('square_feet', 1000)),
            'latitude': float(data.get('latitude', 23.0225)),
            'longitude': float(data.get('longitude', 72.5714)),
            'property_age': int(data.get('property_age', 5))
        }
        
        # Make prediction
        result = predictor_app.predict_price(property_data)
        
        if 'error' in result:
            return jsonify({'success': False, 'error': result['error']}), 400
        
        return jsonify({
            'success': True,
            'prediction': result,
            'input_data': property_data
        })
        
    except Exception as e:
        logger.error(f"Error in predict endpoint: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/model-info')
def model_info():
    """Get model information"""
    return jsonify({
        'model_loaded': predictor_app.model is not None,
        'metadata': predictor_app.metadata,
        'feature_count': len(predictor_app.feature_columns) if predictor_app.feature_columns else 0
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': predictor_app.model is not None,
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    print("🚀 Starting Real Estate Price Prediction Web App...")
    print(f"📁 Model directory: {MODEL_DIR}")
    print(f"🤖 Model loaded: {predictor_app.model is not None}")
    
    if predictor_app.metadata:
        print(f"📊 Model: {predictor_app.metadata.get('model_name')}")
        print(f"📈 R² Score: {predictor_app.metadata.get('r2_score')}")
    
    # Run the Flask app
    app.run(debug=True, host='0.0.0.0', port=5000)
