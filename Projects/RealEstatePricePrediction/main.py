# # Import the modules
# from src.data_processing import DataProcessor
# from src.feature_engineering import FeatureEngineer  
# from src.maps_integration import MapsIntegration

# # Load and process data
# processor = DataProcessor()
# df = processor.load_sample_data()
# df = processor.clean_data(df)

# # Create features
# engineer = FeatureEngineer()
# df = engineer.create_basic_features(df)
# df = engineer.add_simulated_poi_features(df)

# # Create maps
# maps = MapsIntegration("AlzaSy9hE6DyqQBLQyWfJU66HIgwSEkQW2sUBir")
# property_map = maps.create_property_map(df)
# property_map.save("ahmedabad_properties.html")

from src.data_processing import DataProcessor
from src.feature_engineering import FeatureEngineer  
from src.maps_integration import MapsIntegration
from config.config import GOMAPS_API_KEY

def main():
    print("🏠 Starting Ahmedabad Real Estate Price Prediction...")
    
    # Load and process data
    print("📊 Loading and processing data...")
    processor = DataProcessor()
    df = processor.load_sample_data()
    df = processor.clean_data(df)
    print(f"✅ Loaded {len(df)} properties")

    # Create features
    print("🔧 Creating features...")
    engineer = FeatureEngineer()
    df = engineer.create_basic_features(df)
    df = engineer.add_simulated_poi_features(df)
    print(f"✅ Features created: {df.shape[1]} columns")

    # Create maps
    print("🗺️ Creating interactive map...")
    maps = MapsIntegration("AlzaSy9hE6DyqQBLQyWfJU66HIgwSEkQW2sUBir")
    property_map = maps.create_property_map(df)
    property_map.save("ahmedabad_properties.html")
    print("✅ Map saved as 'ahmedabad_properties.html'")
    
    # Display basic statistics
    print(f"\n📈 Dataset Statistics:")
    print(f"   Average Price: ₹{df['price'].mean():,.0f}")
    print(f"   Price Range: ₹{df['price'].min():,.0f} - ₹{df['price'].max():,.0f}")
    print(f"   Average Size: {df['square_feet'].mean():.0f} sq ft")
    
    print("\n🎆 Complete! Open 'ahmedabad_properties.html' in your browser to view the map.")

if __name__ == "__main__":
    main()