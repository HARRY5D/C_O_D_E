"""
Feature Engineering Module for Real Estate Price Prediction
Handles POI calculations, geographic features, and advanced feature creation
"""

import pandas as pd
import numpy as np
from typing import List, Tuple
import warnings
warnings.filterwarnings('ignore')

class FeatureEngineer:
    def __init__(self, gomaps_api_key=None):
        self.gomaps_api_key = gomaps_api_key
        self.api_available = gomaps_api_key is not None
        if not self.api_available:
            print("Warning: GoMaps.pro API key not provided. Some features will be simulated.")
    
    def create_basic_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create basic property features"""
        df = df.copy()
        
        # Age of property
        current_year = 2024
        df['property_age'] = current_year - df['year_built']
        
        # Price per square foot
        df['price_per_sqft'] = df['price'] / df['square_feet']
        
        # Total rooms
        df['total_rooms'] = df['bedrooms'] + df['bathrooms']
        
        # Property size categories
        df['size_category'] = pd.cut(df['square_feet'], 
                                   bins=[0, 1000, 2000, 3000, float('inf')],
                                   labels=['Small', 'Medium', 'Large', 'XLarge'])
        
        # Price categories
        df['price_category'] = pd.cut(df['price'],
                                    bins=5,
                                    labels=['Budget', 'Economy', 'Mid-Range', 'Premium', 'Luxury'])
        
        # Luxury features count
        luxury_features = ['garage', 'pool', 'fireplace']
        df['luxury_score'] = df[luxury_features].sum(axis=1)
        
        return df
    
    def create_location_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create location-based features"""
        df = df.copy()
        
        # Distance from city center (Ahmedabad center: 23.0225, 72.5714)
        city_center_lat, city_center_lng = 23.0225, 72.5714
        
        df['distance_from_center'] = np.sqrt(
            (df['latitude'] - city_center_lat)**2 + 
            (df['longitude'] - city_center_lng)**2
        ) * 111  # Approximate km per degree
        
        # Create neighborhood price statistics
        neighborhood_stats = df.groupby('neighborhood')['price'].agg(['mean', 'median', 'std'])
        neighborhood_stats.columns = ['neighborhood_avg_price', 'neighborhood_median_price', 'neighborhood_price_std']
        df = df.merge(neighborhood_stats, left_on='neighborhood', right_index=True, how='left')
        
        # Relative price position in neighborhood
        df['price_vs_neighborhood'] = df['price'] / df['neighborhood_avg_price']
        
        return df
    
    def add_simulated_poi_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add simulated POI features for demo purposes"""
        df = df.copy()
        
        # Simulate distances to various POIs
        poi_types = ['school', 'hospital', 'shopping_mall', 'park', 'restaurant']
        
        for poi_type in poi_types:
            # Simulate realistic distances based on neighborhood
            if poi_type == 'school':
                df[f'distance_to_{poi_type}'] = np.random.uniform(0.5, 3.0, len(df))
            elif poi_type == 'hospital':
                df[f'distance_to_{poi_type}'] = np.random.uniform(2.0, 8.0, len(df))
            elif poi_type == 'shopping_mall':
                df[f'distance_to_{poi_type}'] = np.random.uniform(1.0, 6.0, len(df))
            elif poi_type == 'park':
                df[f'distance_to_{poi_type}'] = np.random.uniform(0.3, 2.0, len(df))
            elif poi_type == 'restaurant':
                df[f'distance_to_{poi_type}'] = np.random.uniform(0.1, 1.5, len(df))
        
        # Calculate walkability score based on POI distances
        poi_columns = [f'distance_to_{poi}' for poi in poi_types]
        # Inverse relationship: closer POIs = higher walkability
        df['walkability_score'] = 10 - df[poi_columns].mean(axis=1)
        df['walkability_score'] = df['walkability_score'].clip(1, 10)
        
        return df
    
    def create_interaction_features(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create interaction features"""
        df = df.copy()
        
        # Size and age interaction
        df['size_age_interaction'] = df['square_feet'] * df['property_age']
        
        # Location and luxury interaction
        df['location_luxury_score'] = df['walkability_score'] * df['luxury_score']
        
        # Price efficiency metrics
        df['price_efficiency'] = df['square_feet'] / df['price'] * 1000000  # Sqft per lakh
        
        return df

class POIAnalyzer:
    """Analyzes Points of Interest around properties"""
    
    def __init__(self, gomaps_api_key=None):
        self.gomaps_api_key = gomaps_api_key
        self.api_available = gomaps_api_key is not None
    
    def calculate_accessibility_score(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate accessibility score based on POI distances"""
        df = df.copy()
        
        # Define weights for different POI types
        poi_weights = {
            'school': 0.25,
            'hospital': 0.20,
            'shopping_mall': 0.15,
            'park': 0.15,
            'restaurant': 0.10
        }
        
        accessibility_score = 0
        for poi_type, weight in poi_weights.items():
            col_name = f'distance_to_{poi_type}'
            if col_name in df.columns:
                # Convert distance to score (inverse relationship)
                poi_score = 10 / (1 + df[col_name])
                accessibility_score += poi_score * weight
        
        df['accessibility_score'] = accessibility_score
        return df
    
    def create_poi_summary(self, df: pd.DataFrame) -> pd.DataFrame:
        """Create POI summary statistics"""
        poi_columns = [col for col in df.columns if col.startswith('distance_to_')]
        
        if poi_columns:
            df['avg_poi_distance'] = df[poi_columns].mean(axis=1)
            df['min_poi_distance'] = df[poi_columns].min(axis=1)
            df['max_poi_distance'] = df[poi_columns].max(axis=1)
            df['poi_distance_std'] = df[poi_columns].std(axis=1)
        
        return df

def create_comprehensive_features(df: pd.DataFrame, gomaps_api_key=None) -> pd.DataFrame:
    """Create all features in one function"""
    
    print("🔧 Creating comprehensive features...")
    
    # Initialize feature engineer
    engineer = FeatureEngineer(gomaps_api_key)
    poi_analyzer = POIAnalyzer(gomaps_api_key)
    
    # Apply all feature engineering steps
    df = engineer.create_basic_features(df)
    print("   ✅ Basic features created")
    
    df = engineer.create_location_features(df)
    print("   ✅ Location features created")
    
    df = engineer.add_simulated_poi_features(df)
    print("   ✅ POI features added")
    
    df = engineer.create_interaction_features(df)
    print("   ✅ Interaction features created")
    
    df = poi_analyzer.calculate_accessibility_score(df)
    print("   ✅ Accessibility score calculated")
    
    df = poi_analyzer.create_poi_summary(df)
    print("   ✅ POI summary created")
    
    print(f"🎯 Feature engineering complete! Dataset now has {len(df.columns)} columns")
    
    return df

print("✅ Feature Engineering Module Ready!")
print("🏗️ Features: Basic, Location, POI, Interaction, Accessibility")
