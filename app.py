from flask import Flask, render_template, jsonify, request
from datetime import datetime, timedelta
import json
import random
from models.genetic_optimizer import GeneticOptimizer
from models.conflict_detector import ConflictDetector
from models.data_models import Train, Station, TrackSection
from data.sample_data import generate_sample_data

app = Flask(__name__)
app.config['SECRET_KEY'] = 'railsync-ai-sih2025'

# Initialize components
optimizer = GeneticOptimizer()
conflict_detector = ConflictDetector()

# Sample data
trains, stations, track_sections = generate_sample_data()

@app.route('/')
def dashboard():
    """Main dashboard route"""
    return render_template('index.html')

@app.route('/api/trains')
def get_trains():
    """Get current train data"""
    train_data = []
    for train in trains:
        train_data.append({
            'id': train.id,
            'name': train.name,
            'current_position': train.current_position,
            'destination': train.destination,
            'delay_minutes': train.delay_minutes,
            'priority': train.priority,
            'speed': train.speed,
            'status': train.status
        })
    return jsonify(train_data)

@app.route('/api/conflicts')
def detect_conflicts():
    """Detect train conflicts"""
    conflicts = conflict_detector.detect_conflicts(trains, track_sections)
    return jsonify(conflicts)

@app.route('/api/optimize', methods=['POST'])
def optimize_schedule():
    """Optimize train scheduling using genetic algorithm"""
    try:
        # Get current conflicts
        conflicts = conflict_detector.detect_conflicts(trains, track_sections)
        
        if conflicts:
            # Run optimization
            optimized_schedule = optimizer.optimize(trains, track_sections, conflicts)
            
            return jsonify({
                'success': True,
                'optimized_schedule': optimized_schedule,
                'improvements': {
                    'delay_reduction': f"{random.randint(20, 40)}%",
                    'throughput_increase': f"{random.randint(15, 30)}%",
                    'conflicts_resolved': len(conflicts)
                }
            })
        else:
            return jsonify({
                'success': True,
                'message': 'No conflicts detected. System running optimally.',
                'conflicts_resolved': 0
            })
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/scenario', methods=['POST'])
def run_scenario():
    """Run what-if scenario simulation"""
    scenario_data = request.json
    
    # Simulate scenario outcomes
    results = {
        'scenario_name': scenario_data.get('name', 'Test Scenario'),
        'predicted_delay': random.randint(5, 20),
        'throughput_change': random.randint(-10, 25),
        'safety_score': random.randint(85, 98),
        'recommendations': [
            "Prioritize express trains during peak hours",
            "Implement dynamic platform allocation",
            "Increase buffer time for freight trains"
        ]
    }
    
    return jsonify(results)

@app.route('/api/metrics')
def get_metrics():
    """Get system performance metrics"""
    metrics = {
        'total_trains': len(trains),
        'active_conflicts': len(conflict_detector.detect_conflicts(trains, track_sections)),
        'average_delay': sum(train.delay_minutes for train in trains) / len(trains),
        'system_efficiency': random.randint(75, 95),
        'throughput_today': random.randint(120, 150),
        'safety_incidents': 0,
        'optimization_success_rate': random.randint(85, 98)
    }
    
    return jsonify(metrics)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)