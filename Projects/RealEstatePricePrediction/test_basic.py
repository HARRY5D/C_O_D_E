"""
Simple test script for Real Estate ML Platform
Quick verification that all core components work
"""

def test_basic_functionality():
    print("🔬 Testing Real Estate ML Platform - Basic Functionality")
    print("=" * 60)
    
    # Test 1: Import core modules
    print("📦 Testing Core Imports...")
    try:
        import sys
        sys.path.append('src')
        
        from config.config import GOMAPS_API_KEY, DEFAULT_MAP_CENTER
        print("✅ Config loaded")
        
        from src.data_processing import DataProcessor
        print("✅ Data processing imported")
        
        from src.feature_engineering import FeatureEngineer
        print("✅ Feature engineering imported")
        
        from src.maps_integration import MapsIntegration, GoMapsProClient
        print("✅ Maps integration imported")
        
        print("✅ All core modules imported successfully!")
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False
    
    # Test 2: Load and process data
    print("\n📊 Testing Data Processing...")
    try:
        processor = DataProcessor()
        df = processor.load_sample_data()
        df_clean = processor.clean_data(df)
        
        print(f"✅ Loaded {len(df)} properties")
        print(f"✅ Cleaned data: {len(df_clean)} properties")
        print(f"✅ Price range: ₹{df_clean['price'].min():,.0f} - ₹{df_clean['price'].max():,.0f}")
        
    except Exception as e:
        print(f"❌ Data processing error: {e}")
        return False
    
    # Test 3: Feature engineering
    print("\n🔧 Testing Feature Engineering...")
    try:
        engineer = FeatureEngineer()
        df_features = engineer.create_basic_features(df_clean)
        df_features = engineer.create_location_features(df_features)
        df_features = engineer.add_simulated_poi_features(df_features)
        
        print(f"✅ Feature engineering complete: {len(df_features.columns)} columns")
        new_features = [col for col in df_features.columns if col not in df_clean.columns]
        print(f"✅ New features created: {len(new_features)}")
        
    except Exception as e:
        print(f"❌ Feature engineering error: {e}")
        return False
    
    # Test 4: GoMaps.pro API
    print("\n🗺️ Testing GoMaps.pro API...")
    try:
        client = GoMapsProClient(GOMAPS_API_KEY)
        
        # Test geocoding
        result = client.geocode("Ahmedabad, Gujarat, India")
        if result:
            print("✅ Geocoding API working")
        else:
            print("⚠️ Geocoding API returned no results")
        
        # Test places search
        places = client.places_nearby(
            location=(23.0225, 72.5714),
            radius=5000,
            place_type='school'
        )
        if places:
            print(f"✅ Places API working - Found {len(places)} schools")
        else:
            print("⚠️ Places API returned no results")
            
    except Exception as e:
        print(f"❌ GoMaps API error: {e}")
        return False
    
    # Test 5: Basic ML Model
    print("\n🤖 Testing Basic ML Model...")
    try:
        from sklearn.ensemble import RandomForestRegressor
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import r2_score
        
        # Prepare data for ML
        feature_columns = [col for col in df_features.columns 
                          if col not in ['price', 'property_id', 'description'] 
                          and df_features[col].dtype in ['int64', 'float64']]
        
        X = df_features[feature_columns].fillna(0)
        y = df_features['price']
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Train model
        model = RandomForestRegressor(n_estimators=10, random_state=42)
        model.fit(X_train, y_train)
        
        # Evaluate
        y_pred = model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        
        print(f"✅ Random Forest trained successfully")
        print(f"✅ Model R² score: {r2:.3f}")
        
    except Exception as e:
        print(f"❌ ML model error: {e}")
        return False
    
    # Test 6: Visualization
    print("\n📊 Testing Visualization...")
    try:
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        # Simple price distribution plot
        plt.figure(figsize=(8, 4))
        plt.hist(df_features['price'], bins=20, alpha=0.7)
        plt.title('Property Price Distribution')
        plt.xlabel('Price (₹)')
        plt.ylabel('Count')
        plt.close()  # Don't show the plot, just test that it works
        
        print("✅ Matplotlib visualization working")
        
        # Test folium maps
        import folium
        m = folium.Map(location=DEFAULT_MAP_CENTER, zoom_start=12)
        print("✅ Folium maps working")
        
    except Exception as e:
        print(f"❌ Visualization error: {e}")
        return False
    
    print("\n" + "=" * 60)
    print("🎉 ALL BASIC TESTS PASSED!")
    print("\n📋 Your Real Estate ML Platform is ready!")
    print("\n🚀 Next Steps:")
    print("1. Run: jupyter notebook")
    print("2. Open: notebooks/real_estate_ml_platform.ipynb")
    print("3. Execute all cells to start the full platform")
    print("\n🏠 Happy real estate analyzing! 🏠")
    
    return True

if __name__ == "__main__":
    test_basic_functionality()
