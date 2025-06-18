"""
GoMaps.pro Integration Module for Real Estate Price Prediction
Handles map visualization, geocoding, and interactive features using GoMaps.pro API
"""

import folium
from folium import plugins
import pandas as pd
import numpy as np
import requests
import json
from typing import List, Tuple, Dict, Optional
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import time

class GoMapsProClient:
    """Client for GoMaps.pro API services"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://maps.gomaps.pro/maps/api"
        
    def geocode(self, address: str) -> Optional[Dict]:
        """Geocode an address using GoMaps.pro"""
        url = f"{self.base_url}/geocode/json"
        params = {
            'address': address,
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'OK' and data['results']:
                    return data['results'][0]
            return None
        except Exception as e:
            print(f"Geocoding error: {e}")
            return None
    
    def reverse_geocode(self, lat: float, lng: float) -> Optional[Dict]:
        """Reverse geocode coordinates using GoMaps.pro"""
        url = f"{self.base_url}/geocode/json"
        params = {
            'latlng': f"{lat},{lng}",
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'OK' and data['results']:
                    return data['results'][0]
            return None
        except Exception as e:
            print(f"Reverse geocoding error: {e}")
            return None
    
    def places_nearby(self, location: Tuple[float, float], radius: int = 5000, 
                     place_type: str = 'school') -> List[Dict]:
        """Find nearby places using GoMaps.pro Places API"""
        url = f"{self.base_url}/place/nearbysearch/json"
        params = {
            'location': f"{location[0]},{location[1]}",
            'radius': radius,
            'type': place_type,
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'OK':
                    return data['results']
            return []
        except Exception as e:
            print(f"Places search error: {e}")
            return []
    
    def distance_matrix(self, origins: List[Tuple[float, float]], 
                       destinations: List[Tuple[float, float]], 
                       mode: str = 'driving') -> Optional[Dict]:
        """Calculate distance matrix using GoMaps.pro"""
        url = f"{self.base_url}/distancematrix/json"
        
        origins_str = '|'.join([f"{lat},{lng}" for lat, lng in origins])
        destinations_str = '|'.join([f"{lat},{lng}" for lat, lng in destinations])
        
        params = {
            'origins': origins_str,
            'destinations': destinations_str,
            'mode': mode,
            'key': self.api_key
        }
        
        try:
            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'OK':
                    return data
            return None
        except Exception as e:
            print(f"Distance matrix error: {e}")
            return None

class MapsIntegration:
    """Maps integration using GoMaps.pro API for real estate applications"""
    
    def __init__(self, gomaps_api_key: str):
        self.api_key = gomaps_api_key
        self.client = GoMapsProClient(gomaps_api_key)
    def create_property_map(self, df: pd.DataFrame, center_coords: Tuple[float, float] = None):
        """Create an interactive map with property locations"""
        # Always use Ahmedabad coordinates as center for this platform
        if center_coords is None:
            # Use Ahmedabad city center coordinates
            center_coords = (23.0225, 72.5714)  # Ahmedabad, Gujarat, India
        
        print(f"📍 Creating map centered on Ahmedabad: {center_coords}")
        
        # Create base map centered on Ahmedabad
        m = folium.Map(
            location=center_coords,
            zoom_start=11,  # Good zoom level for city view
            tiles='OpenStreetMap'
        )
        
        # Add property markers
        for idx, row in df.iterrows():
            # Color coding based on price
            price = row.get('price', 0)
            if price < df['price'].quantile(0.33):
                color = 'green'
                icon = 'home'
            elif price < df['price'].quantile(0.66):
                color = 'orange'
                icon = 'home'
            else:
                color = 'red'
                icon = 'star'
            
            # Create popup content with Indian Rupee formatting
            popup_content = f"""
            <div style="width: 250px;">
                <h4>Property Details</h4>
                <p><b>Price:</b> ₹{price:,.0f}</p>
                <p><b>Bedrooms:</b> {row.get('bedrooms', 'N/A')}</p>
                <p><b>Bathrooms:</b> {row.get('bathrooms', 'N/A')}</p>
                <p><b>Square Feet:</b> {row.get('square_feet', 'N/A'):,}</p>
                <p><b>Property Type:</b> {row.get('property_type', 'N/A')}</p>
                <p><b>Neighborhood:</b> {row.get('neighborhood', 'N/A')}</p>
                <p><b>Year Built:</b> {row.get('year_built', 'N/A')}</p>
            </div>
            """
            
            folium.Marker(
                location=[row['latitude'], row['longitude']],
                popup=folium.Popup(popup_content, max_width=300),
                tooltip=f"₹{price:,.0f}",
                icon=folium.Icon(color=color, icon=icon)
            ).add_to(m)
        
        # Add a heatmap layer for price density
        heat_data = [[row['latitude'], row['longitude'], row.get('price', 0)/100000] 
                    for idx, row in df.iterrows()]
        
        plugins.HeatMap(heat_data, name='Price Heatmap', show=False).add_to(m)
        
        # Add layer control
        folium.LayerControl().add_to(m)
        
        return m
    
    def create_price_distribution_map(self, df: pd.DataFrame):
        """Create a choropleth map showing price distribution by neighborhood"""
        fig = px.scatter_mapbox(
            df, 
            lat='latitude', 
            lon='longitude',
            color='price',
            size='square_feet',
            hover_data=['bedrooms', 'bathrooms', 'property_type', 'neighborhood'],
            color_continuous_scale='Viridis',
            title='Property Price Distribution in Ahmedabad',
            mapbox_style='open-street-map',
            zoom=10
        )
        
        fig.update_layout(
            height=600,
            margin={"r":0,"t":50,"l":0,"b":0},
            mapbox=dict(
                center=dict(lat=23.0225, lon=72.5714),
                zoom=10
            )
        )
        
        return fig
    
    def geocode_address(self, address: str) -> Tuple[float, float]:
        """Convert address to coordinates using GoMaps.pro"""
        result = self.client.geocode(address)
        if result:
            location = result['geometry']['location']
            return (location['lat'], location['lng'])
        return None
    
    def reverse_geocode(self, coordinates: Tuple[float, float]) -> str:
        """Convert coordinates to address using GoMaps.pro"""
        result = self.client.reverse_geocode(coordinates[0], coordinates[1])
        if result:
            return result['formatted_address']
        return f"Address at {coordinates[0]:.4f}, {coordinates[1]:.4f}"
    
    def add_poi_markers(self, map_obj: folium.Map, center_coords: Tuple[float, float], 
                       poi_types: List[str], radius: int = 5000):
        """Add POI markers to the map using GoMaps.pro"""
        colors = ['blue', 'purple', 'darkgreen', 'cadetblue', 'darkblue', 
                 'lightgreen', 'orange', 'lightblue', 'pink']
        
        for i, poi_type in enumerate(poi_types):
            color = colors[i % len(colors)]
            
            try:
                places = self.client.places_nearby(
                    location=center_coords,
                    radius=radius,
                    place_type=poi_type
                )
                
                for place in places[:10]:
                    poi_location = place['geometry']['location']
                    
                    folium.Marker(
                        location=[poi_location['lat'], poi_location['lng']],
                        popup=f"{place['name']} ({poi_type})",
                        tooltip=place['name'],
                        icon=folium.Icon(color=color, icon='info-sign')
                    ).add_to(map_obj)
                    
            except Exception as e:
                print(f"Error adding {poi_type} markers: {e}")
        
        return map_obj

def calculate_poi_distances_gomaps(properties_df: pd.DataFrame, 
                                  poi_types: List[str],
                                  api_key: str) -> pd.DataFrame:
    """Calculate distances to POIs using GoMaps.pro API"""
    
    client = GoMapsProClient(api_key)
    df = properties_df.copy()
    
    print("🔍 Calculating POI distances using GoMaps.pro...")
    
    for poi_type in poi_types:
        print(f"   📍 Processing {poi_type}...")
        distances = []
        
        for idx, row in df.iterrows():
            try:
                places = client.places_nearby(
                    location=(row['latitude'], row['longitude']),
                    radius=5000,
                    place_type=poi_type
                )
                
                if places:
                    property_location = [(row['latitude'], row['longitude'])]
                    place_locations = [
                        (place['geometry']['location']['lat'], 
                         place['geometry']['location']['lng'])
                        for place in places[:5]
                    ]
                    
                    distance_result = client.distance_matrix(
                        origins=property_location,
                        destinations=place_locations
                    )
                    
                    if distance_result and distance_result['rows']:
                        elements = distance_result['rows'][0]['elements']
                        valid_distances = [
                            elem['distance']['value'] for elem in elements
                            if elem['status'] == 'OK'
                        ]
                        
                        if valid_distances:
                            min_distance = min(valid_distances)
                            distances.append(min_distance)
                        else:
                            distances.append(np.nan)
                    else:
                        distances.append(np.nan)
                else:
                    distances.append(np.nan)
                    
                time.sleep(0.1)
                
            except Exception as e:
                print(f"Error processing {poi_type} for property {idx}: {e}")
                distances.append(np.nan)
        
        df[f'distance_to_{poi_type}'] = distances
    
    return df

def get_location_info_gomaps(address: str, api_key: str) -> Dict:
    """Get detailed location information using GoMaps.pro"""
    
    client = GoMapsProClient(api_key)
    
    geocode_result = client.geocode(address)
    
    if not geocode_result:
        return {'error': 'Address not found'}
    
    location = geocode_result['geometry']['location']
    lat, lng = location['lat'], location['lng']
    
    amenities = {}
    poi_types = ['school', 'hospital', 'shopping_mall', 'park', 'restaurant']
    
    for poi_type in poi_types:
        places = client.places_nearby(
            location=(lat, lng),
            radius=2000,
            place_type=poi_type
        )
        amenities[f'nearby_{poi_type}s'] = len(places)
    
    return {
        'latitude': lat,
        'longitude': lng,
        'formatted_address': geocode_result['formatted_address'],
        'amenities': amenities,
        'place_id': geocode_result.get('place_id', '')
    }

print("✅ GoMaps.pro Maps Integration Module Ready!")
print("📍 Features: Property Maps, POI Analysis, Distance Calculations")
print("🗺️ API: GoMaps.pro integration for Ahmedabad real estate")