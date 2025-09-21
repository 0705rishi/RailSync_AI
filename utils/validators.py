"""
Data validation utilities for RailSync AI
"""

import re
from typing import Dict, List, Any, Optional
from datetime import datetime

def validate_train_data(train_data: Dict) -> tuple[bool, List[str]]:
    """Validate train data structure and values"""
    errors = []
    
    # Required fields
    required_fields = ['id', 'name', 'current_position', 'destination']
    for field in required_fields:
        if not train_data.get(field):
            errors.append(f"Missing required field: {field}")
    
    # Validate train ID format
    train_id = train_data.get('id', '')
    if train_id and not re.match(r'^TRN\d{3}$', train_id):
        errors.append("Train ID must be in format TRN### (e.g., TRN001)")
    
    # Validate speed
    speed = train_data.get('speed', 0)
    if not isinstance(speed, (int, float)) or speed < 0 or speed > 200:
        errors.append("Speed must be between 0 and 200 km/h")
    
    # Validate priority
    priority = train_data.get('priority', 1)
    if not isinstance(priority, int) or priority < 1 or priority > 5:
        errors.append("Priority must be an integer between 1 and 5")
    
    # Validate delay
    delay = train_data.get('delay_minutes', 0)
    if not isinstance(delay, (int, float)) or delay < 0:
        errors.append("Delay must be a non-negative number")
    
    return len(errors) == 0, errors

def validate_station_data(station_data: Dict) -> tuple[bool, List[str]]:
    """Validate station data structure and values"""
    errors = []
    
    # Required fields
    required_fields = ['id', 'name']
    for field in required_fields:
        if not station_data.get(field):
            errors.append(f"Missing required field: {field}")
    
    # Validate station ID format
    station_id = station_data.get('id', '')
    if station_id and not re.match(r'^STN\d{3}$', station_id):
        errors.append("Station ID must be in format STN### (e.g., STN001)")
    
    # Validate platforms
    platforms = station_data.get('platforms', 4)
    if not isinstance(platforms, int) or platforms < 1 or platforms > 20:
        errors.append("Platforms must be between 1 and 20")
    
    return len(errors) == 0, errors

def validate_track_section_data(track_data: Dict) -> tuple[bool, List[str]]:
    """Validate track section data structure and values"""
    errors = []
    
    # Required fields
    required_fields = ['id', 'name', 'start_station', 'end_station']
    for field in required_fields:
        if not track_data.get(field):
            errors.append(f"Missing required field: {field}")
    
    # Validate track ID format
    track_id = track_data.get('id', '')
    if track_id and not re.match(r'^TRK\d{3}$', track_id):
        errors.append("Track ID must be in format TRK### (e.g., TRK001)")
    
    # Validate capacity
    capacity = track_data.get('capacity', 2)
    if not isinstance(capacity, int) or capacity < 1 or capacity > 10:
        errors.append("Track capacity must be between 1 and 10")
    
    # Validate start and end stations are different
    start = track_data.get('start_station', '')
    end = track_data.get('end_station', '')
    if start and end and start == end:
        errors.append("Start and end stations must be different")
    
    return len(errors) == 0, errors

def validate_optimization_parameters(params: Dict) -> tuple[bool, List[str]]:
    """Validate genetic algorithm parameters"""
    errors = []
    
    # Population size
    pop_size = params.get('population_size', 50)
    if not isinstance(pop_size, int) or pop_size < 10 or pop_size > 200:
        errors.append("Population size must be between 10 and 200")
    
    # Generations
    generations = params.get('generations', 30)
    if not isinstance(generations, int) or generations < 5 or generations > 100:
        errors.append("Generations must be between 5 and 100")
    
    # Mutation rate
    mutation_rate = params.get('mutation_rate', 0.1)
    if not isinstance(mutation_rate, (int, float)) or mutation_rate < 0 or mutation_rate > 1:
        errors.append("Mutation rate must be between 0.0 and 1.0")
    
    return len(errors) == 0, errors

def validate_api_request(request_data: Dict, required_fields: List[str]) -> tuple[bool, List[str]]:
    """Generic API request validation"""
    errors = []
    
    if not isinstance(request_data, dict):
        errors.append("Request data must be a JSON object")
        return False, errors
    
    # Check required fields
    for field in required_fields:
        if field not in request_data:
            errors.append(f"Missing required field: {field}")
        elif request_data[field] is None or request_data[field] == "":
            errors.append(f"Field '{field}' cannot be empty")
    
    return len(errors) == 0, errors

def sanitize_input(input_string: str) -> str:
    """Sanitize user input to prevent injection attacks"""
    if not isinstance(input_string, str):
        return str(input_string)
    
    # Remove potentially harmful characters
    sanitized = re.sub(r'[<>"\';]', '', input_string)
    
    # Limit length
    sanitized = sanitized[:255]
    
    # Strip whitespace
    return sanitized.strip()

def is_valid_train_name(name: str) -> bool:
    """Check if train name follows valid format"""
    if not name or len(name) < 3:
        return False
    
    # Should contain letters and may contain numbers, spaces, hyphens
    pattern = r'^[A-Za-z][A-Za-z0-9\s\-]+$'
    return bool(re.match(pattern, name))

def is_valid_time_format(time_str: str) -> bool:
    """Validate time string format (HH:MM)"""
    pattern = r'^([01]?[0-9]|2[0-3]):[0-5][0-9]$'
    return bool(re.match(pattern, time_str))

def validate_coordinates(lat: float, lon: float) -> bool:
    """Validate latitude and longitude coordinates"""
    try:
        lat = float(lat)
        lon = float(lon)
        return -90 <= lat <= 90 and -180 <= lon <= 180
    except (ValueError, TypeError):
        return False