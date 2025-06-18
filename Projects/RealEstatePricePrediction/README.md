# Real Estate Price Prediction Platform

A comprehensive machine learning platform for predicting real estate prices with Google Maps integration.

## Features

- **Property Price Prediction**: ML models for accurate price estimation
- **Google Maps Integration**: Location analysis and visualization
- **POI Distance Calculation**: Distance to points of interest
- **Feature Importance Analysis**: Understanding key pricing factors
- **NLP Analysis**: Property description sentiment and feature extraction
- **Interactive Visualizations**: Maps, charts, and prediction insights

## Project Structure

```
RealEstatePricePrediction/
├── notebooks/
│   └── real_estate_ml_platform.ipynb    # Main Jupyter notebook
├── src/
│   ├── data_processing.py               # Data preprocessing utilities
│   ├── feature_engineering.py          # Feature creation and POI calculations
│   ├── ml_models.py                     # Machine learning models
│   ├── maps_integration.py              # Google Maps API integration
│   ├── nlp_analysis.py                  # NLP for property descriptions
│   └── visualization.py                 # Plotting and visualization utilities
├── data/
│   ├── sample_data.csv                  # Sample real estate data
│   └── poi_data.csv                     # Points of interest data
├── config/
│   └── config.py                        # Configuration and API keys
└── requirements.txt                     # Python dependencies
```

## Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Add your Google Maps API key to `config/config.py`
3. Run the Jupyter notebook: `jupyter notebook notebooks/real_estate_ml_platform.ipynb`

## Google Maps in Jupyter

Yes, Google Maps works perfectly in Jupyter notebooks using:
- **Folium**: Interactive maps with markers and popups
- **ipywidgets**: Interactive controls and forms
- **Google Maps JavaScript API**: Embedded maps with full functionality
- **Plotly**: Geographic visualizations and scatter maps

The platform uses multiple visualization approaches to ensure compatibility and rich interactive experiences.
