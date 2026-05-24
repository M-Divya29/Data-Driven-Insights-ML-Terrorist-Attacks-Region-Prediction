import folium
import requests
import math
import random
import os
import logging

logger = logging.getLogger(__name__)

# Function to get route from OpenRouteService
def get_route(api_key, start_coords, end_coords):
    """
    Fetch route data from OpenRouteService API
    
    Args:
        api_key: OpenRouteService API key
        start_coords: tuple (latitude, longitude)
        end_coords: tuple (latitude, longitude)
    
    Returns:
        Response JSON or None if failed
    """
    try:
        url = "https://api.openrouteservice.org/v2/directions/driving-car"
        headers = {"Authorization": api_key}
        params = {
            "start": f"{start_coords[1]},{start_coords[0]}",
            "end": f"{end_coords[1]},{end_coords[0]}"
        }
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"Route API error: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        logger.error(f"Error fetching route: {e}")
        return None

# Function to calculate the bearing between two points
def calculate_bearing(lat1, lon1, lat2, lon2):
    """Calculate compass bearing between two geographic points"""
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    x = math.sin(dlon) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - math.sin(lat1) * math.cos(lat2) * math.cos(dlon)
    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360
    return compass_bearing

# Function to get potential attack zones with threat level and suggestions
def find_potential_attack_zones(route_coords, threshold=45):
    """
    Identify potential vulnerable zones along route based on bearing changes
    
    Args:
        route_coords: List of (latitude, longitude) tuples
        threshold: Bearing change threshold in degrees
    
    Returns:
        List of (coordinates, threat_level, suggestion, radius)
    """
    attack_zones = []
    for i in range(1, len(route_coords) - 1):
        lat1, lon1 = route_coords[i - 1]
        lat2, lon2 = route_coords[i]
        lat3, lon3 = route_coords[i + 1]
        
        bearing1 = calculate_bearing(lat1, lon1, lat2, lon2)
        bearing2 = calculate_bearing(lat2, lon2, lat3, lon3)
        bearing_diff = abs(bearing2 - bearing1)
        
        # Random threat level (for demonstration)
        threat_level = random.randint(10, 90)
        
        # Suggestion logic based on threat level
        if threat_level <= 20:
            suggestion = "Low threat area. Normal vigilance recommended."
            radius = 100
        elif 20 < threat_level <= 40:
            suggestion = "Moderate threat possible. Stay alert."
            radius = 200
        elif 40 < threat_level <= 60:
            suggestion = "High threat potential. Avoid if possible."
            radius = 300
        elif 60 < threat_level <= 80:
            suggestion = "Very high threat area. Extreme caution required."
            radius = 400
        else:
            suggestion = "Critical threat zone! Avoid this area completely."
            radius = 500
        
        if bearing_diff > threshold:
            attack_zones.append((route_coords[i], threat_level, suggestion, radius))
    
    return attack_zones

def GetMap(From, To):
    """
    Generate map with route and threat zones
    
    Args:
        From: List [latitude, longitude] of starting point
        To: List [latitude, longitude] of destination
    
    Returns:
        True if successful, False otherwise
    """
    try:
        source_lat = float(From[0])
        source_lon = float(From[1])
        destination_lat = float(To[0])
        destination_lon = float(To[1])
        
        # Get API key from environment
        api_key = os.environ.get("OPENROUTE_API_KEY")
        if not api_key:
            logger.error("OPENROUTE_API_KEY not set in environment")
            return False
        
        route_data = get_route(api_key, (source_lat, source_lon), (destination_lat, destination_lon))
        
        if not route_data:
            logger.error("Failed to fetch route data")
            return False
        
        # Extract coordinates from response
        coordinates = route_data.get('features', [{}])[0].get('geometry', {}).get('coordinates', [])
        if not coordinates:
            logger.error("No coordinates in route data")
            return False
        
        route_coords = [(lat, lon) for lon, lat in coordinates]
        attack_zones = find_potential_attack_zones(route_coords)
        
        # Create map centered at source
        m = folium.Map(location=[source_lat, source_lon], zoom_start=12)
        
        # Draw the route
        folium.PolyLine(route_coords, color="blue", weight=5, opacity=0.8).add_to(m)
        
        # Add source and destination markers
        folium.Marker(
            [source_lat, source_lon],
            popup="Source",
            icon=folium.Icon(color="green")
        ).add_to(m)
        
        folium.Marker(
            [destination_lat, destination_lon],
            popup="Destination",
            icon=folium.Icon(color="red")
        ).add_to(m)
        
        # Add attack zones as red transparent circles
        for point, threat_level, suggestion, radius in attack_zones:
            folium.Circle(
                location=point,
                radius=radius,
                popup=f"Threat Level: {threat_level}%<br>Suggestion: {suggestion}",
                color="red",
                fill=True,
                fill_color="red",
                fill_opacity=0.3,
                weight=1
            ).add_to(m)
        
        # Save map
        map_path = "static/route_map.html"
        os.makedirs("static", exist_ok=True)
        m.save(map_path)
        logger.info(f"Map saved to {map_path}")
        
        return True
    
    except ValueError as e:
        logger.error(f"Invalid coordinate values: {e}")
        return False
    except Exception as e:
        logger.error(f"Error generating map: {e}")
        return False
