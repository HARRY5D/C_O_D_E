# """
# Test script to verify Google Maps API key functionality
# """

# import googlemaps
# import requests
# from config.config import GOOGLE_MAPS_API_KEY

# def test_google_maps_api():
#     """Test if the Google Maps API key works with required services"""
    
#     print("🔑 Testing Google Maps API Key...")
#     print(f"API Key: {GOOGLE_MAPS_API_KEY[:10]}...{GOOGLE_MAPS_API_KEY[-4:]}")
#     print("=" * 50)
    
#     # Test 1: Basic API key validation
#     try:
#         gmaps = googlemaps.Client(key=GOOGLE_MAPS_API_KEY)
#         print("✅ API key format is valid")
#     except Exception as e:
#         print(f"❌ API key format error: {e}")
#         return False
    
#     # Test 2: Geocoding API
#     try:
#         geocode_result = gmaps.geocode("Ahmedabad, Gujarat, India")
#         if geocode_result:
#             print("✅ Geocoding API is working")
#             location = geocode_result[0]['geometry']['location']
#             print(f"   Ahmedabad coordinates: {location['lat']}, {location['lng']}")
#         else:
#             print("❌ Geocoding API returned no results")
#     except Exception as e:
#         print(f"❌ Geocoding API error: {e}")
    
#     # Test 3: Places API (nearby search)
#     try:
#         places_result = gmaps.places_nearby(
#             location=(23.0225, 72.5714),  # Ahmedabad coordinates
#             radius=5000,
#             type='school'
#         )
#         if places_result['results']:
#             print("✅ Places API is working")
#             print(f"   Found {len(places_result['results'])} schools near Ahmedabad")
#         else:
#             print("❌ Places API returned no results")
#     except Exception as e:
#         print(f"❌ Places API error: {e}")
#         if "REQUEST_DENIED" in str(e):
#             print("   💡 This usually means Places API is not enabled for your key")
    
#     # Test 4: Distance Matrix API
#     try:
#         origins = [(23.0225, 72.5714)]  # Ahmedabad
#         destinations = [(23.0300, 72.5800)]  # Nearby location
        
#         distance_result = gmaps.distance_matrix(
#             origins=origins,
#             destinations=destinations,
#             mode="driving"
#         )
        
#         if distance_result['status'] == 'OK':
#             print("✅ Distance Matrix API is working")
#         else:
#             print(f"❌ Distance Matrix API error: {distance_result['status']}")
#     except Exception as e:
#         print(f"❌ Distance Matrix API error: {e}")
    
#     print("\n🎯 API Test Complete!")
#     print("\nIf you see errors above, you may need to:")
#     print("1. Enable the required APIs in Google Cloud Console")
#     print("2. Set up billing (required even for free tier)")
#     print("3. Check API key restrictions")
#     print("4. Verify quota limits")

# if __name__ == "__main__":
#     test_google_maps_api()


"""
Test script to verify GoMaps.pro API key functionality
"""

import requests
import json
from config.config import GOOGLE_MAPS_API_KEY

def test_gomaps_pro_api():
    """Test if the GoMaps.pro API key works"""
    
    print("🔑 Testing GoMaps.pro API Key...")
    print(f"API Key: {GOOGLE_MAPS_API_KEY[:10]}...{GOOGLE_MAPS_API_KEY[-4:]}")
    print("=" * 50)
    
    # Test 1: Geocoding API
    try:
        url = "https://maps.gomaps.pro/maps/api/geocode/json"
        params = {
            'address': 'Ahmedabad, Gujarat, India',
            'key': GOOGLE_MAPS_API_KEY
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                print("✅ GoMaps.pro Geocoding API is working")
                location = data['results'][0]['geometry']['location']
                print(f"   Ahmedabad coordinates: {location['lat']}, {location['lng']}")
            else:
                print(f"❌ Geocoding API error: {data['status']}")
                if 'error_message' in data:
                    print(f"   Error message: {data['error_message']}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Geocoding API error: {e}")
    
    # Test 2: Places API (nearby search)
    try:
        url = "https://maps.gomaps.pro/maps/api/place/nearbysearch/json"
        params = {
            'location': '23.0225,72.5714',  # Ahmedabad coordinates
            'radius': 5000,
            'type': 'school',
            'key': GOOGLE_MAPS_API_KEY
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                print("✅ GoMaps.pro Places API is working")
                print(f"   Found {len(data['results'])} schools near Ahmedabad")
            else:
                print(f"❌ Places API error: {data['status']}")
                if 'error_message' in data:
                    print(f"   Error message: {data['error_message']}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Places API error: {e}")
    
    # Test 3: Distance Matrix API
    try:
        url = "https://maps.gomaps.pro/maps/api/distancematrix/json"
        params = {
            'origins': '23.0225,72.5714',
            'destinations': '23.0300,72.5800',
            'mode': 'driving',
            'key': GOOGLE_MAPS_API_KEY
        }
        
        response = requests.get(url, params=params)
        
        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                print("✅ GoMaps.pro Distance Matrix API is working")
            else:
                print(f"❌ Distance Matrix API error: {data['status']}")
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Distance Matrix API error: {e}")
    
    print("\n🎯 GoMaps.pro API Test Complete!")

if __name__ == "__main__":
    test_gomaps_pro_api()