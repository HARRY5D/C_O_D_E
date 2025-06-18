"""
Test script for Real Estate ML Platform
Tests all modules and GoMaps.pro integration
"""

import sys
import os
sys.path.append('src')

# Test imports
def test_imports():
    print("🔬 Testing Module Imports...")
    
    try:
        from config.config import GOMAPS_API_KEY, DEFAULT_MAP_CENTER
        print("✅ Config module imported")
        
        from src.data_processing import DataProcessor
        print("✅ Data processing module imported")
        
        from src.feature_engineering import FeatureEngineer, POIAnalyzer
        print("✅ Feature engineering module imported")
        
        from src.ml_models import MLModelManager, ModelExplainer
        print("✅ ML models module imported")
        
        from src.maps_integration import MapsIntegration, GoMapsProClient
        print("✅ Maps integration module imported")
        
        from src.nlp_analysis import PropertyDescriptionAnalyzer
        print("✅ NLP analysis module imported")
        
        from src.visualization import RealEstateVisualizer
        print("✅ Visualization module imported")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

# Test data loading
def test_data_loading():
    print("\n📊 Testing Data Loading...")
    
    try:
        from src.data_processing import DataProcessor
        
        processor = DataProcessor()
        df = processor.load_sample_data()
        
        print(f"✅ Loaded {len(df)} properties")
        print(f"✅ Columns: {list(df.columns)}")
        print(f"✅ Price range: ₹{df['price'].min():,.0f} - ₹{df['price'].max():,.0f}")
        
        return df
        
    except Exception as e:
        print(f"❌ Data loading error: {e}")
        return None

# Test GoMaps.pro API
def test_gomaps_api():
    print("\n🗺️ Testing GoMaps.pro API...")
    
    try:
        from config.config import GOMAPS_API_KEY
        from src.maps_integration import GoMapsProClient
        
        client = GoMapsProClient(GOMAPS_API_KEY)
        
        # Test geocoding
        result = client.geocode("Vastrapur, Ahmedabad, Gujarat, India")
        if result:
            print("✅ Geocoding API working")
            print(f"   📍 Vastrapur coordinates: {result['geometry']['location']}")
        else:
            print("❌ Geocoding API failed")
            return False
        
        # Test places search
        places = client.places_nearby(
            location=(23.0225, 72.5714),
            radius=5000,
            place_type='school'
        )
        if places:
            print(f"✅ Places API working - Found {len(places)} schools")
        else:
            print("❌ Places API failed")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ GoMaps API error: {e}")
        return False

# Test ML models
def test_ml_models():
    print("\n🤖 Testing ML Models...")
    
    try:
        from src.data_processing import DataProcessor
        from src.feature_engineering import FeatureEngineer
        from src.ml_models import MLModelManager
        
        # Load and process data
        processor = DataProcessor()
        df = processor.load_sample_data()
        df = processor.clean_data(df)
        
        # Engineer features
        engineer = FeatureEngineer()
        df = engineer.create_basic_features(df)
        
        # Train models
        manager = MLModelManager()
        results = manager.train_multiple_models(df)
        
        print(f"✅ Trained {len(results)} ML models")
        for model_name, metrics in results.items():
            print(f"   📈 {model_name}: R² = {metrics['r2']:.3f}")
        
        return True
        
    except Exception as e:
        print(f"❌ ML models error: {e}")
        return False

# Main test function
def run_all_tests():
    print("🚀 Real Estate ML Platform - Comprehensive Test Suite")
    print("=" * 60)
    
    # Test 1: Module imports
    if not test_imports():
        print("\n❌ Test failed at imports. Please check module structure.")
        return False
    
    # Test 2: Data loading
    df = test_data_loading()
    if df is None:
        print("\n❌ Test failed at data loading.")
        return False
    
    # Test 3: GoMaps.pro API
    if not test_gomaps_api():
        print("\n❌ Test failed at GoMaps.pro API. Check API key and internet connection.")
        return False
    
    # Test 4: ML models
    if not test_ml_models():
        print("\n❌ Test failed at ML models.")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ALL TESTS PASSED! Your platform is ready to use!")
    print("\n📋 Next Steps:")
    print("1. Open Jupyter Notebook: jupyter notebook")
    print("2. Navigate to: notebooks/real_estate_ml_platform.ipynb")
    print("3. Run all cells to start the platform")
    print("\n🏠 Happy real estate analyzing! 🏠")
    
    return True

if __name__ == "__main__":
    run_all_tests()
