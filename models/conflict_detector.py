from datetime import datetime, timedelta
import math

class ConflictDetector:
    def __init__(self):
        self.safety_buffer = 5  # minutes
        self.distance_threshold = 2  # km
        
    def detect_conflicts(self, trains, track_sections):
        """Detect potential conflicts between trains"""
        conflicts = []
        
        # Check for spatial conflicts (same track section)
        spatial_conflicts = self._detect_spatial_conflicts(trains, track_sections)
        conflicts.extend(spatial_conflicts)
        
        # Check for temporal conflicts (timing issues)
        temporal_conflicts = self._detect_temporal_conflicts(trains)
        conflicts.extend(temporal_conflicts)
        
        # Check for junction conflicts
        junction_conflicts = self._detect_junction_conflicts(trains, track_sections)
        conflicts.extend(junction_conflicts)
        
        return conflicts
    
    def _detect_spatial_conflicts(self, trains, track_sections):
        """Detect trains on collision course in same track section"""
        conflicts = []
        
        for i, train1 in enumerate(trains):
            for j, train2 in enumerate(trains[i+1:], i+1):
                if self._are_trains_conflicting(train1, train2):
                    conflict = {
                        'type': 'spatial_conflict',
                        'severity': 'high',
                        'trains': [train1.id, train2.id],
                        'train_names': [train1.name, train2.name],
                        'location': self._get_conflict_location(train1, train2),
                        'estimated_time': self._estimate_conflict_time(train1, train2),
                        'description': f"Potential collision between {train1.name} and {train2.name}"
                    }
                    conflicts.append(conflict)
                    
        return conflicts
    
    def _detect_temporal_conflicts(self, trains):
        """Detect scheduling conflicts due to timing"""
        conflicts = []
        
        # Group trains by destination/route
        route_groups = {}
        for train in trains:
            route = train.destination
            if route not in route_groups:
                route_groups[route] = []
            route_groups[route].append(train)
        
        # Check for conflicts within each route
        for route, route_trains in route_groups.items():
            if len(route_trains) > 1:
                # Sort by expected arrival time
                route_trains.sort(key=lambda t: t.current_position)
                
                for i in range(len(route_trains) - 1):
                    train1 = route_trains[i]
                    train2 = route_trains[i + 1]
                    
                    # Check if trains are too close in time
                    time_gap = self._calculate_time_gap(train1, train2)
                    if time_gap < self.safety_buffer:
                        conflict = {
                            'type': 'temporal_conflict',
                            'severity': 'medium',
                            'trains': [train1.id, train2.id],
                            'train_names': [train1.name, train2.name],
                            'time_gap': time_gap,
                            'required_gap': self.safety_buffer,
                            'description': f"Insufficient time gap between {train1.name} and {train2.name}"
                        }
                        conflicts.append(conflict)
                        
        return conflicts
    
    def _detect_junction_conflicts(self, trains, track_sections):
        """Detect conflicts at railway junctions"""
        conflicts = []
        
        # Identify trains approaching junctions
        junction_trains = {}
        
        for train in trains:
            # Simulate junction detection based on position
            if 'junction' in train.current_position.lower() or train.current_position.endswith('_JN'):
                junction = train.current_position
                if junction not in junction_trains:
                    junction_trains[junction] = []
                junction_trains[junction].append(train)
        
        # Check for conflicts at each junction
        for junction, trains_at_junction in junction_trains.items():
            if len(trains_at_junction) > 1:
                for i, train1 in enumerate(trains_at_junction):
                    for train2 in trains_at_junction[i+1:]:
                        conflict = {
                            'type': 'junction_conflict',
                            'severity': 'high',
                            'trains': [train1.id, train2.id],
                            'train_names': [train1.name, train2.name],
                            'junction': junction,
                            'description': f"Junction conflict at {junction} between {train1.name} and {train2.name}"
                        }
                        conflicts.append(conflict)
                        
        return conflicts
    
    def _are_trains_conflicting(self, train1, train2):
        """Check if two trains are on collision course"""
        # Simple conflict detection based on position and direction
        if train1.current_position == train2.current_position:
            return True
            
        # Check if trains are moving towards each other
        if train1.destination == train2.current_position and train2.destination == train1.current_position:
            return True
            
        return False
    
    def _get_conflict_location(self, train1, train2):
        """Get estimated conflict location"""
        # Simple implementation - use midpoint
        return f"Between {train1.current_position} and {train2.current_position}"
    
    def _estimate_conflict_time(self, train1, train2):
        """Estimate time until conflict occurs"""
        # Simple calculation based on speed and distance
        base_time = 10  # minutes
        speed_factor = (train1.speed + train2.speed) / 120  # normalize to average speed
        return max(2, int(base_time / speed_factor))
    
    def _calculate_time_gap(self, train1, train2):
        """Calculate time gap between two trains"""
        # Simple calculation based on position difference and speed
        position_diff = abs(hash(train1.current_position) - hash(train2.current_position)) % 20
        avg_speed = (train1.speed + train2.speed) / 2
        time_gap = (position_diff / avg_speed) * 60  # convert to minutes
        return max(1, int(time_gap))