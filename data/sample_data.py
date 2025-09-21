from models.data_models import Train, Station, TrackSection

def generate_sample_data():
    """Generate sample railway data for demonstration"""
    
    # Sample stations
    stations = [
        Station('STN001', 'New Delhi', 16),
        Station('STN002', 'Mumbai Central', 12),
        Station('STN003', 'Chennai Central', 10),
        Station('STN004', 'Kolkata', 14),
        Station('STN005', 'Bangalore City', 8),
        Station('STN006', 'Hyderabad', 6),
        Station('STN007', 'Pune Junction', 6),
        Station('STN008', 'Ahmedabad', 8)
    ]
    
    # Sample trains
    trains = [
        Train('TRN001', 'Rajdhani Express', 'New Delhi', 'Mumbai Central', 3),
        Train('TRN002', 'Shatabdi Express', 'Mumbai Central', 'Pune Junction', 2),
        Train('TRN003', 'Duronto Express', 'Chennai Central', 'New Delhi', 3),
        Train('TRN004', 'Gatimaan Express', 'New Delhi', 'Agra Cantt', 2),
        Train('TRN005', 'Vande Bharat', 'Mumbai Central', 'Ahmedabad', 3),
        Train('TRN006', 'Chennai Express', 'Chennai Central', 'Mumbai Central', 2),
        Train('TRN007', 'Howrah Express', 'Kolkata', 'New Delhi', 2),
        Train('TRN008', 'Bangalore Express', 'Bangalore City', 'Chennai Central', 1),
        Train('TRN009', 'Hyderabad Express', 'Hyderabad', 'New Delhi', 2),
        Train('TRN010', 'Freight Special', 'Mumbai Central', 'Kolkata', 1)
    ]
    
    # Sample track sections
    track_sections = [
        TrackSection('TRK001', 'Delhi-Mumbai Main Line', 'New Delhi', 'Mumbai Central', 3),
        TrackSection('TRK002', 'Mumbai-Pune Section', 'Mumbai Central', 'Pune Junction', 2),
        TrackSection('TRK003', 'Chennai-Bangalore Line', 'Chennai Central', 'Bangalore City', 2),
        TrackSection('TRK004', 'Delhi-Kolkata Route', 'New Delhi', 'Kolkata', 2),
        TrackSection('TRK005', 'Mumbai-Ahmedabad Line', 'Mumbai Central', 'Ahmedabad', 2),
        TrackSection('TRK006', 'Hyderabad Junction', 'Hyderabad', 'New Delhi', 1)
    ]
    
    return trains, stations, track_sections