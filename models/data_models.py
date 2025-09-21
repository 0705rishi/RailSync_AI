from datetime import datetime
import random

class Train:
    def __init__(self, train_id, name, current_position, destination, priority=1):
        self.id = train_id
        self.name = name
        self.current_position = current_position
        self.destination = destination
        self.priority = priority
        self.delay_minutes = random.randint(0, 30)
        self.speed = random.randint(60, 120)  # km/h
        self.status = self._generate_status()
        
    def _generate_status(self):
        statuses = ['On Time', 'Delayed', 'Approaching', 'At Platform']
        if self.delay_minutes > 15:
            return 'Delayed'
        elif self.delay_minutes > 5:
            return 'Approaching'
        else:
            return random.choice(['On Time', 'At Platform'])

class Station:
    def __init__(self, station_id, name, platforms=4):
        self.id = station_id
        self.name = name
        self.platforms = platforms
        self.current_occupancy = random.randint(0, platforms)

class TrackSection:
    def __init__(self, section_id, name, start_station, end_station, capacity=2):
        self.id = section_id
        self.name = name
        self.start_station = start_station
        self.end_station = end_station
        self.capacity = capacity
        self.current_trains = random.randint(0, capacity)
        self.signals = self._generate_signals()
        
    def _generate_signals(self):
        signal_states = ['Green', 'Yellow', 'Red']
        return {
            'entry': random.choice(signal_states),
            'exit': random.choice(signal_states)
        }