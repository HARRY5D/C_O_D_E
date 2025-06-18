"""
Data Processing Module for Real Estate Price Prediction
Handles data loading, cleaning, and preprocessing
"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

class DataProcessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_columns = []
        
    def load_sample_data(self, n_samples=1000):
        """Generate sample real estate data for demonstration"""
        np.random.seed(42)
          # Generate synthetic data for Ahmedabad, India
        data = {
            'bedrooms': np.random.randint(1, 6, n_samples),
            'bathrooms': np.random.randint(1, 4, n_samples),
            'square_feet': np.random.randint(500, 5000, n_samples),
            'lot_size': np.random.randint(1000, 20000, n_samples),
            'year_built': np.random.randint(1950, 2024, n_samples),
            'latitude': np.random.uniform(22.9, 23.15, n_samples),  # Ahmedabad latitude range
            'longitude': np.random.uniform(72.4, 72.75, n_samples),  # Ahmedabad longitude range
            'property_type': np.random.choice(['House', 'Condo', 'Townhouse'], n_samples),
            'neighborhood': np.random.choice(['Vastrapur', 'Bopal', 'Chandkheda', 'Naranpura', 'Prahlad Nagar', 'SG Highway', 'Maninagar', 'Satellite'], n_samples),
            'garage': np.random.choice([0, 1, 2], n_samples),
            'pool': np.random.choice([0, 1], n_samples, p=[0.8, 0.2]),
            'fireplace': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
        }
        
        df = pd.DataFrame(data)
          # Generate realistic prices in Indian Rupees based on features
        base_price = 2500000  # Base price in INR (25 lakhs)
        price = (base_price + 
                df['bedrooms'] * 800000 +      # 8 lakhs per bedroom
                df['bathrooms'] * 400000 +     # 4 lakhs per bathroom  
                df['square_feet'] * 2500 +     # 2500 INR per sq ft
                df['lot_size'] * 100 +         # 100 INR per sq ft lot
                (2024 - df['year_built']) * -30000 +  # Depreciation
                df['garage'] * 500000 +        # 5 lakhs for garage
                df['pool'] * 800000 +          # 8 lakhs for pool
                df['fireplace'] * 300000 +     # 3 lakhs for fireplace
                np.random.normal(0, 500000, n_samples))  # Random variation
          # Neighborhood adjustments for Ahmedabad areas
        neighborhood_multiplier = {
            'Vastrapur': 2.2,      # Premium area
            'Bopal': 1.8,          # Growing upscale area  
            'Prahlad Nagar': 2.0,  # High-end residential
            'SG Highway': 1.9,     # Commercial and premium residential
            'Satellite': 1.6,      # Established area
            'Chandkheda': 1.2,     # Developing area
            'Naranpura': 1.4,      # Central location
            'Maninagar': 1.0       # Traditional area
        }
        df['price'] = price * df['neighborhood'].map(neighborhood_multiplier)
        df['price'] = np.maximum(df['price'], 1500000)  # Minimum price 15 lakhs INR
          # Add property descriptions suitable for Ahmedabad
        descriptions = [
            "Beautiful family home with modern amenities in prime location",
            "Spacious property with great connectivity and peaceful environment", 
            "Well-designed home with excellent ventilation and natural light",
            "Ready to move property with premium finishes and parking",
            "Cozy home in developing area with good investment potential",
            "Luxurious property with all modern conveniences",
            "Family-friendly home near schools and shopping centers",
            "Elegant property with traditional and modern design elements"
        ]
        df['description'] = np.random.choice(descriptions, n_samples)
        
        return df
    
    def clean_data(self, df):
        """Clean and preprocess the data"""
        # Handle missing values
        numeric_columns = df.select_dtypes(include=[np.number]).columns
        df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())
        
        categorical_columns = df.select_dtypes(include=['object']).columns
        for col in categorical_columns:
            df[col] = df[col].fillna(df[col].mode()[0])
        
        # Remove outliers using IQR method
        for col in ['price', 'square_feet', 'lot_size']:
            if col in df.columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 1.5 * IQR
                upper_bound = Q3 + 1.5 * IQR
                df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        
        return df
    
    def encode_categorical_features(self, df):
        """Encode categorical variables"""
        categorical_columns = df.select_dtypes(include=['object']).columns
        categorical_columns = [col for col in categorical_columns if col != 'description']
        
        for col in categorical_columns:
            if col not in self.label_encoders:
                self.label_encoders[col] = LabelEncoder()
                df[col] = self.label_encoders[col].fit_transform(df[col])
            else:
                df[col] = self.label_encoders[col].transform(df[col])
        
        return df
    
    def create_features(self, df):
        """Create additional features"""
        # Age of property
        df['property_age'] = 2024 - df['year_built']
        
        # Price per square foot
        df['price_per_sqft'] = df['price'] / df['square_feet']
        
        # Bathroom to bedroom ratio
        df['bath_bed_ratio'] = df['bathrooms'] / df['bedrooms']
        
        # Total rooms
        df['total_rooms'] = df['bedrooms'] + df['bathrooms']
        
        # Luxury score (combination of features)
        df['luxury_score'] = (df['pool'] * 2 + df['fireplace'] + 
                             (df['garage'] > 0).astype(int) + 
                             (df['square_feet'] > 3000).astype(int))
        
        return df
    
    def prepare_features(self, df, target_column='price'):
        """Prepare features for machine learning"""
        # Separate features and target
        if target_column in df.columns:
            y = df[target_column]
            X = df.drop([target_column, 'description'], axis=1, errors='ignore')
        else:
            y = None
            X = df.drop(['description'], axis=1, errors='ignore')
        
        # Store feature columns
        self.feature_columns = X.columns.tolist()
        
        return X, y
    
    def scale_features(self, X_train, X_test=None):
        """Scale numerical features"""
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_train_scaled = pd.DataFrame(X_train_scaled, columns=X_train.columns, index=X_train.index)
        
        if X_test is not None:
            X_test_scaled = self.scaler.transform(X_test)
            X_test_scaled = pd.DataFrame(X_test_scaled, columns=X_test.columns, index=X_test.index)
            return X_train_scaled, X_test_scaled
        
        return X_train_scaled
    
    def split_data(self, X, y, test_size=0.2, random_state=42):
        """Split data into training and testing sets"""
        return train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    def process_pipeline(self, df, target_column='price'):
        """Complete preprocessing pipeline"""
        print("Starting data processing pipeline...")
        
        # Clean data
        df_clean = self.clean_data(df.copy())
        print(f"Data cleaned. Shape: {df_clean.shape}")
        
        # Encode categorical features
        df_encoded = self.encode_categorical_features(df_clean)
        print("Categorical features encoded.")
        
        # Create additional features
        df_features = self.create_features(df_encoded)
        print("Additional features created.")
        
        # Prepare features
        X, y = self.prepare_features(df_features, target_column)
        print(f"Features prepared. Shape: {X.shape}")
        
        return X, y, df_features
