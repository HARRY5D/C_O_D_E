"""
Real Data Processor for Ahmedabad Property Dataset
Handles loading and processing of the actual ahmedabad.csv file
"""

import pandas as pd
import numpy as np
import re
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class RealDataProcessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = []
        
    def process_real_ahmedabad_data(self, df_raw):
        """Process the real Ahmedabad CSV dataset"""
        print("🔧 Processing real Ahmedabad property data...")
        
        # Create a copy for processing
        df = df_raw.copy()
        
        # Extract property details from title
        df = self._extract_property_details(df)
        
        # Clean and convert price
        df = self._clean_price_data(df)
        
        # Extract area information
        df = self._extract_area_info(df)
        
        # Extract location information
        df = self._extract_location_info(df)
        
        # Generate coordinates for Ahmedabad locations
        df = self._add_coordinates(df)
        
        # Create additional features
        df = self._create_additional_features(df)
        
        # Clean and validate data
        df = self._clean_final_data(df)
        
        print(f"✅ Processed {len(df)} properties successfully")
        print(f"📊 Features: {list(df.columns)}")
        
        return df
    
    def _extract_property_details(self, df):
        """Extract BHK, property type, and other details from title"""
        df['bedrooms'] = df['Title'].str.extract(r'(\d+)\s*BHK').astype(float)
        
        # Extract property type
        property_types = ['Apartment', 'Villa', 'Bungalow', 'Row House', 'Penthouse', 'House', 'Flat']
        df['property_type'] = 'Apartment'  # Default
        
        for prop_type in property_types:
            mask = df['Title'].str.contains(prop_type, case=False, na=False)
            df.loc[mask, 'property_type'] = prop_type
        
        return df
    
    def _clean_price_data(self, df):
        """Clean and convert price from 'XX Lac' format to numeric"""
        def convert_price(price_str):
            if pd.isna(price_str):
                return np.nan
            
            # Remove currency symbols and extract number
            price_str = str(price_str).replace('₹', '').replace(',', '').strip()
            
            # Handle "XX Lac" format
            if 'Lac' in price_str or 'lac' in price_str:
                numbers = re.findall(r'[\d.]+', price_str)
                if numbers:
                    return float(numbers[0]) * 100000  # Convert lac to rupees
            
            # Handle "XX Crore" format
            if 'Crore' in price_str or 'crore' in price_str:
                numbers = re.findall(r'[\d.]+', price_str)
                if numbers:
                    return float(numbers[0]) * 10000000  # Convert crore to rupees
            
            # Direct number
            numbers = re.findall(r'[\d.]+', price_str)
            if numbers:
                return float(numbers[0])
            
            return np.nan
        
        df['price'] = df['price'].apply(convert_price)
        return df
    
    def _extract_area_info(self, df):
        """Extract area information from value_area column"""
        def extract_area(area_str):
            if pd.isna(area_str):
                return np.nan
            
            area_str = str(area_str)
            # Extract valid numbers from area string (must have at least one digit)
            numbers = re.findall(r'\d+\.?\d*', area_str)
            if numbers:
                try:
                    area = float(numbers[0])
                    
                    # Convert different units to square feet
                    if 'sqyrd' in area_str.lower() or 'sq yrd' in area_str.lower():
                        return area * 9  # 1 sq yard = 9 sq feet
                    elif 'sqft' in area_str.lower() or 'sq ft' in area_str.lower():
                        return area
                    else:
                        return area  # Assume sq ft if no unit specified
                except ValueError:
                    return np.nan
            
            return np.nan
        
        df['square_feet'] = df['value_area'].apply(extract_area)
        return df
    
    def _extract_location_info(self, df):
        """Extract neighborhood information from title"""
        # Common Ahmedabad areas
        ahmedabad_areas = [
            'Vastrapur', 'Satellite', 'Bopal', 'Maninagar', 'Navrangpura',
            'Prahladnagar', 'Thaltej', 'Gota', 'Shela', 'Chandkheda',
            'Sarkhej', 'Jodhpur', 'Ambawadi', 'Ellis Bridge', 'Ashram Road',
            'Zundal', 'Sanand', 'Ghuma', 'Jagatpur', 'Vastral', 'Nikol',
            'Ranip', 'Naroda', 'Odhav', 'Vatva', 'CTM', 'Amraiwadi',
            'Behrampura', 'Sughad', 'Narolgam', 'Vejalpur', 'Jivraj Park'
        ]
        
        df['neighborhood'] = 'Other'  # Default
        
        for area in ahmedabad_areas:
            mask = df['Title'].str.contains(area, case=False, na=False)
            df.loc[mask, 'neighborhood'] = area
        
        return df
    
    def _add_coordinates(self, df):
        """Add latitude and longitude based on neighborhood"""
        # Ahmedabad area coordinates (approximate)
        area_coords = {
            'Vastrapur': (23.0395, 72.5299),
            'Satellite': (23.0318, 72.5120),
            'Bopal': (23.0473, 72.4284),
            'Maninagar': (22.9965, 72.5992),
            'Navrangpura': (23.0395, 72.5659),
            'Prahladnagar': (23.0477, 72.5074),
            'Thaltej': (23.0477, 72.5074),
            'Gota': (23.1089, 72.5661),
            'Shela': (23.0473, 72.4284),
            'Chandkheda': (23.1544, 72.6381),
            'Sarkhej': (23.0015, 72.4885),
            'Jodhpur': (23.0477, 72.5074),
            'Ambawadi': (23.0318, 72.5659),
            'Ellis Bridge': (23.0395, 72.5659),
            'Ashram Road': (23.0318, 72.5659),
            'Zundal': (23.1089, 72.6381),
            'Sanand': (22.9790, 72.3840),
            'Ghuma': (23.0473, 72.4284),
            'Jagatpur': (23.1089, 72.5661),
            'Vastral': (23.0477, 72.6381),
            'Nikol': (23.0836, 72.6381),
            'Ranip': (23.0836, 72.5661),
            'Naroda': (23.0836, 72.6381),
            'Other': (23.0225, 72.5714)  # Ahmedabad center
        }
        
        # Add some random variation to coordinates
        np.random.seed(42)
        coords = [area_coords.get(area, area_coords['Other']) for area in df['neighborhood']]
        
        df['latitude'] = [coord[0] + np.random.normal(0, 0.01) for coord in coords]
        df['longitude'] = [coord[1] + np.random.normal(0, 0.01) for coord in coords]
        
        return df
    
    def _create_additional_features(self, df):
        """Create additional features for ML"""
        
        # Bathrooms (estimate based on bedrooms)
        df['bathrooms'] = df['bedrooms'].fillna(2)
        df.loc[df['bedrooms'] == 1, 'bathrooms'] = 1
        df.loc[df['bedrooms'] >= 3, 'bathrooms'] = df['bedrooms'] - 1
        
        # Year built (estimate based on status)
        current_year = 2024
        df['year_built'] = current_year - 5  # Default 5 years old
        
        # New properties
        new_mask = df['status'].str.contains('New Property', na=False)
        df.loc[new_mask, 'year_built'] = current_year
        
        # Ready to move properties
        ready_mask = df['status'].str.contains('Ready to Move', na=False)
        df.loc[ready_mask, 'year_built'] = current_year - np.random.randint(1, 10, sum(ready_mask))
        
        # Possession dates
        poss_mask = df['status'].str.contains('Poss. by', na=False)
        df.loc[poss_mask, 'year_built'] = current_year + 1
        
        # Property age
        df['property_age'] = current_year - df['year_built']
        
        # Price per square foot
        df['price_per_sqft'] = df['price'] / df['square_feet']
        
        # Furnishing binary features
        df['is_furnished'] = df['furnishing'].str.contains('Furnished', na=False).astype(int)
        df['is_semi_furnished'] = df['furnishing'].str.contains('Semi-Furnished', na=False).astype(int)
        
        # Transaction type
        df['is_resale'] = df['transaction'].str.contains('Resale', na=False).astype(int)
        
        # Floor information
        df['floor_number'] = df['floor'].str.extract(r'(\d+)').astype(float).fillna(1)
        
        # Add some synthetic features for demonstration
        df['garage'] = np.random.choice([0, 1, 2], len(df), p=[0.3, 0.5, 0.2])
        df['pool'] = np.random.choice([0, 1], len(df), p=[0.8, 0.2])
        df['fireplace'] = np.random.choice([0, 1], len(df), p=[0.7, 0.3])
        df['lot_size'] = df['square_feet'] * np.random.uniform(1.5, 3.0, len(df))
        
        return df
    
    def _clean_final_data(self, df):
        """Final data cleaning and validation"""
        
        # Remove rows with missing critical data
        df = df.dropna(subset=['price', 'square_feet', 'bedrooms'])
        
        # Remove outliers
        for col in ['price', 'square_feet']:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        
        # Ensure reasonable values
        df = df[df['price'] > 500000]  # Minimum 5 lakh
        df = df[df['price'] < 50000000]  # Maximum 5 crore
        df = df[df['square_feet'] > 200]  # Minimum 200 sq ft
        df = df[df['square_feet'] < 10000]  # Maximum 10000 sq ft
        df = df[df['bedrooms'] <= 5]  # Maximum 5 bedrooms
        
        # Fill remaining missing values
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())
        
        categorical_columns = df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            df[col] = df[col].fillna(df[col].mode()[0] if not df[col].mode().empty else 'Unknown')
        
        return df
    
    def prepare_features_for_ml(self, df):
        """Prepare features for machine learning"""
        
        # Select relevant columns for ML
        feature_columns = [
            'bedrooms', 'bathrooms', 'square_feet', 'lot_size', 'year_built',
            'property_age', 'floor_number', 'garage', 'pool', 'fireplace',
            'is_furnished', 'is_semi_furnished', 'is_resale',
            'latitude', 'longitude'
        ]
        
        # Add encoded categorical features
        categorical_features = ['neighborhood', 'property_type']
        
        for col in categorical_features:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                df[f'{col}_encoded'] = self.label_encoders[col].fit_transform(df[col])
            else:
                df[f'{col}_encoded'] = self.label_encoders[col].transform(df[col])
            
            feature_columns.append(f'{col}_encoded')
        
        # Prepare feature matrix
        X = df[feature_columns]
        y = df['price']
        
        self.feature_columns = feature_columns
        
        print(f"✅ Features prepared: {len(feature_columns)} features")
        print(f"Features: {feature_columns}")
        
        return X, y
    
    def create_train_test_split(self, X, y, test_size=0.2, random_state=42):
        """Create train-test split"""
        return train_test_split(X, y, test_size=test_size, random_state=random_state)

# Test the processor
if __name__ == "__main__":
    processor = RealDataProcessor()
    
    # Load the CSV file
    try:
        df_raw = pd.read_csv('../data/ahmedabad.csv')
        print(f"✅ Loaded {len(df_raw)} properties from CSV")
        
        # Process the data
        df_processed = processor.process_real_ahmedabad_data(df_raw)
        
        # Prepare for ML
        X, y = processor.prepare_features_for_ml(df_processed)
        print(f"✅ ML features prepared: {X.shape}")
        print(f"Price range: ₹{y.min():,.0f} - ₹{y.max():,.0f}")
        
    except FileNotFoundError:
        print("❌ CSV file not found. Please ensure 'ahmedabad.csv' is in the data directory.")
    except Exception as e:
        print(f"❌ Error processing data: {e}")
