# Configuration file for Real Estate ML Platform

# GoMaps.pro API Configuration
GOMAPS_API_KEY = "AlzaSy9hE6DyqQBLQyWfJU66HIgwSEkQW2sUBir"

# Map Configuration
DEFAULT_MAP_CENTER = [23.0225, 72.5714]  # Ahmedabad, Gujarat, India
DEFAULT_ZOOM_LEVEL = 12

# Model Configuration
MODEL_PARAMS = {
    'random_forest': {
        'n_estimators': 100,
        'max_depth': 10,
        'random_state': 42
    },
    'xgboost': {
        'n_estimators': 100,
        'max_depth': 6,
        'learning_rate': 0.1,
        'random_state': 42
    },
    'lightgbm': {
        'n_estimators': 100,
        'max_depth': 6,
        'learning_rate': 0.1,
        'random_state': 42
    },
    'catboost': {
        'iterations': 100,
        'depth': 6,
        'learning_rate': 0.1,
        'random_state': 42,
        'verbose': False
    }
}

# Feature Engineering Configuration
FEATURE_PARAMS = {
    'poi_types': ['school', 'hospital', 'shopping_mall', 'park', 'restaurant'],
    'max_distance': 5000,  # meters
    'price_bins': 5
}

# Data Processing Configuration
RANDOM_STATE = 42
TEST_SIZE = 0.2

# API Rate Limiting (GoMaps.pro specific)
API_DELAY = 0.1  # Seconds between API calls
MAX_RETRIES = 3

# File Paths
DATA_PATH = "data/"
MODEL_PATH = "models/"
OUTPUT_PATH = "output/"

# Visualization Configuration
PLOT_STYLE = 'seaborn-v0_8'
FIGURE_SIZE = (12, 8)
DPI = 300

# Price formatting (Indian Rupees)
CURRENCY_SYMBOL = "₹"
PRICE_SCALE = 1  # No scaling needed for INR

print("✅ Configuration loaded successfully!")
print(f"🗺️ Using GoMaps.pro API for Ahmedabad real estate analysis")