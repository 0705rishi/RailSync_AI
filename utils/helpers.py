"""
Helper functions for RailSync AI system
"""

import random
import string
import math
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

def generate_id(prefix: str = "", length: int = 6) -> str:
    """Generate a unique ID with optional prefix"""
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return f"{prefix}{suffix}" if prefix else suffix

def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Calculate distance between two coordinates using Haversine formula"""
    # Convert latitude and longitude to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    # Radius of earth in kilometers
    r = 6371
    return c * r

def format_time(minutes: int) -> str:
    """Format minutes into human-readable time string"""
    if minutes < 60:
        return f"{minutes}m"
    
    hours = minutes // 60
    remaining_minutes = minutes % 60
    
    if remaining_minutes == 0:
        return f"{hours}h"
    else:
        return f"{hours}h {remaining_minutes}m"

def calculate_eta(distance_km: float, speed_kmh: float, delay_minutes: int = 0) -> datetime:
    """Calculate estimated time of arrival"""
    travel_time_hours = distance_km / speed_kmh
    travel_time_minutes = travel_time_hours * 60
    
    eta = datetime.now() + timedelta(minutes=travel_time_minutes + delay_minutes)
    return eta

def parse_train_number(train_name: str) -> Optional[str]:
    """Extract train number from train name"""
    import re
    pattern = r'\b(\d{4,5})\b'
    match = re.search(pattern, train_name)
    return match.group(1) if match else None

def get_priority_level(priority: int) -> str:
    """Convert numeric priority to descriptive level"""
    if priority >= 3:
        return "High"
    elif priority == 2:
        return "Medium"
    else:
        return "Low"

def calculate_efficiency(total_time: float, optimal_time: float) -> float:
    """Calculate system efficiency percentage"""
    if optimal_time <= 0:
        return 0.0
    return min(100.0, (optimal_time / total_time) * 100)

def generate_sample_coordinates() -> tuple:
    """Generate sample coordinates for testing"""
    # Sample coordinates around major Indian cities
    base_coords = [
        (28.6139, 77.2090),  # Delhi
        (19.0760, 72.8777),  # Mumbai  
        (13.0827, 80.2707),  # Chennai
        (22.5726, 88.3639),  # Kolkata
        (12.9716, 77.5946),  # Bangalore
        (17.3850, 78.4867),  # Hyderabad
    ]
    
    base_lat, base_lon = random.choice(base_coords)
    
    # Add small random offset
    lat_offset = random.uniform(-0.1, 0.1)
    lon_offset = random.uniform(-0.1, 0.1)
    
    return (base_lat + lat_offset, base_lon + lon_offset)

def create_response(success: bool, data: Any = None, message: str = "", error: str = "") -> Dict:
    """Create standardized API response"""
    response = {
        'success': success,
        'timestamp': datetime.now().isoformat()
    }
    
    if success:
        response['data'] = data
        if message:
            response['message'] = message
    else:
        response['error'] = error or "An error occurred"
    
    return response

def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """Safe division that handles zero denominator"""
    try:
        return numerator / denominator if denominator != 0 else default
    except (TypeError, ZeroDivisionError):
        return default

def clamp(value: float, min_value: float, max_value: float) -> float:
    """Clamp value between min and max"""
    return max(min_value, min(value, max_value))

def get_train_type(train_name: str) -> str:
    """Determine train type from name"""
    name_lower = train_name.lower()
    
    if 'rajdhani' in name_lower:
        return 'Rajdhani'
    elif 'shatabdi' in name_lower:
        return 'Shatabdi'
    elif 'duronto' in name_lower:
        return 'Duronto'
    elif 'express' in name_lower:
        return 'Express'
    elif 'local' in name_lower:
        return 'Local'
    elif 'freight' in name_lower:
        return 'Freight'
    elif 'vande bharat' in name_lower:
        return 'Vande Bharat'
    else:
        return 'Passenger'

def estimate_fuel_consumption(distance_km: float, speed_kmh: float, train_type: str) -> float:
    """Estimate fuel consumption in liters"""
    # Base consumption rates (liters per km)
    consumption_rates = {
        'Freight': 3.5,
        'Express': 2.8,
        'Rajdhani': 2.5,
        'Shatabdi': 2.2,
        'Vande Bharat': 1.8,
        'Local': 2.0,
        'Passenger': 2.5
    }
    
    base_rate = consumption_rates.get(train_type, 2.5)
    
    # Speed factor (higher speed = more consumption)
    speed_factor = 1.0 + (speed_kmh - 80) * 0.01
    speed_factor = clamp(speed_factor, 0.8, 1.5)
    
    return distance_km * base_rate * speed_factor