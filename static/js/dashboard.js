// RailSync AI Dashboard JavaScript

let refreshInterval;

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadMetrics();
    loadTrains();
    detectConflicts();
    
    // Auto-refresh every 30 seconds
    refreshInterval = setInterval(() => {
        loadMetrics();
        loadTrains();
        detectConflicts();
    }, 30000);
});

// Load system metrics
async function loadMetrics() {
    try {
        const response = await fetch('/api/metrics');
        const metrics = await response.json();
        
        document.getElementById('total-trains').textContent = metrics.total_trains;
        document.getElementById('active-conflicts').textContent = metrics.active_conflicts;
        document.getElementById('average-delay').textContent = `${metrics.average_delay.toFixed(1)}min`;
        document.getElementById('system-efficiency').textContent = `${metrics.system_efficiency}%`;
        document.getElementById('throughput-today').textContent = metrics.throughput_today;
        document.getElementById('ai-success-rate').textContent = `${metrics.optimization_success_rate}%`;
        
    } catch (error) {
        console.error('Error loading metrics:', error);
    }
}

// Load train data
async function loadTrains() {
    try {
        const response = await fetch('/api/trains');
        const trains = await response.json();
        
        const trainList = document.getElementById('train-list');
        trainList.innerHTML = '';
        
        trains.forEach(train => {
            const statusClass = getStatusClass(train.status);
            const trainCard = `
                <div class="train-item mb-2 p-2 border rounded">
                    <div class="d-flex justify-content-between">
                        <div>
                            <strong>${train.name}</strong>
                            <br>
                            <small class="text-muted">${train.current_position} → ${train.destination}</small>
                        </div>
                        <div class="text-end">
                            <span class="badge bg-${statusClass}">${train.status}</span>
                            <br>
                            <small class="text-muted">${train.delay_minutes}min delay</small>
                        </div>
                    </div>
                    <div class="mt-2">
                        <div class="progress" style="height: 5px;">
                            <div class="progress-bar bg-info" style="width: ${(train.speed / 120) * 100}%"></div>
                        </div>
                        <small class="text-muted">${train.speed} km/h</small>
                    </div>
                </div>
            `;
            trainList.innerHTML += trainCard;
        });
        
    } catch (error) {
        console.error('Error loading trains:', error);
        document.getElementById('train-list').innerHTML = '<div class="text-danger">Error loading train data</div>';
    }
}

// Detect conflicts
async function detectConflicts() {
    try {
        const response = await fetch('/api/conflicts');
        const conflicts = await response.json();
        
        const conflictList = document.getElementById('conflict-list');
        conflictList.innerHTML = '';
        
        if (conflicts.length === 0) {
            conflictList.innerHTML = '<div class="text-success text-center">No conflicts detected</div>';
            return;
        }
        
        conflicts.forEach(conflict => {
            const severityClass = getSeverityClass(conflict.severity);
            const conflictCard = `
                <div class="alert alert-${severityClass} mb-2">
                    <div class="d-flex justify-content-between">
                        <div>
                            <strong>${conflict.type.replace('_', ' ').toUpperCase()}</strong>
                            <br>
                            <small>${conflict.description}</small>
                        </div>
                        <div class="text-end">
                            <span class="badge bg-${severityClass}">${conflict.severity}</span>
                            ${conflict.estimated_time ? `<br><small>${conflict.estimated_time} min</small>` : ''}
                        </div>
                    </div>
                </div>
            `;
            conflictList.innerHTML += conflictCard;
        });
        
    } catch (error) {
        console.error('Error detecting conflicts:', error);
        document.getElementById('conflict-list').innerHTML = '<div class="text-danger">Error detecting conflicts</div>';
    }
}

// Run AI optimization
async function runOptimization() {
    const button = event.target;
    const originalText = button.innerHTML;
    
    button.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Optimizing...';
    button.disabled = true;
    
    try {
        const response = await fetch('/api/optimize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        const result = await response.json();
        
        const recommendationsDiv = document.getElementById('recommendations');
        
        if (result.success) {
            let html = `
                <div class="alert alert-success">
                    <strong>Optimization Complete!</strong>
                    <ul class="mb-0 mt-2">
                        <li>Delay Reduction: ${result.improvements.delay_reduction}</li>
                        <li>Throughput Increase: ${result.improvements.throughput_increase}</li>
                        <li>Conflicts Resolved: ${result.improvements.conflicts_resolved}</li>
                    </ul>
                </div>
            `;
            
            if (result.optimized_schedule && result.optimized_schedule.length > 0) {
                html += '<h6>Recommendations:</h6>';
                result.optimized_schedule.forEach(schedule => {
                    html += `
                        <div class="recommendation-item mb-2 p-2 border rounded">
                            <strong>${schedule.train_name}</strong>
                            <br>
                            <small class="text-muted">${schedule.recommendation}</small>
                            <br>
                            <span class="badge bg-info">Priority: ${schedule.priority}</span>
                            <span class="badge bg-secondary">Platform: ${schedule.platform}</span>
                        </div>
                    `;
                });
            }
            
            recommendationsDiv.innerHTML = html;
        } else {
            recommendationsDiv.innerHTML = `<div class="alert alert-danger">${result.error}</div>`;
        }
        
    } catch (error) {
        console.error('Error running optimization:', error);
        document.getElementById('recommendations').innerHTML = '<div class="text-danger">Error running optimization</div>';
    } finally {
        button.innerHTML = originalText;
        button.disabled = false;
    }
}

// Run scenario simulation
async function runScenario() {
    const scenarioName = document.getElementById('scenario-name').value || 'Test Scenario';
    const scenarioType = document.getElementById('scenario-type').value;
    
    try {
        const response = await fetch('/api/scenario', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name: scenarioName,
                type: scenarioType
            })
        });
        
        const result = await response.json();
        
        const resultsDiv = document.getElementById('scenario-results');
        resultsDiv.innerHTML = `
            <div class="alert alert-info">
                <h6>Scenario Results: ${result.scenario_name}</h6>
                <div class="row">
                    <div class="col-md-4">
                        <strong>Predicted Delay:</strong> ${result.predicted_delay} min
                    </div>
                    <div class="col-md-4">
                        <strong>Throughput Change:</strong> ${result.throughput_change > 0 ? '+' : ''}${result.throughput_change}%
                    </div>
                    <div class="col-md-4">
                        <strong>Safety Score:</strong> ${result.safety_score}%
                    </div>
                </div>
                <h6 class="mt-3">Recommendations:</h6>
                <ul class="mb-0">
                    ${result.recommendations.map(rec => `<li>${rec}</li>`).join('')}
                </ul>
            </div>
        `;
        
    } catch (error) {
        console.error('Error running scenario:', error);
        document.getElementById('scenario-results').innerHTML = '<div class="text-danger">Error running scenario</div>';
    }
}

// Refresh trains manually
function refreshTrains() {
    loadTrains();
    loadMetrics();
}

// Helper functions
function getStatusClass(status) {
    switch(status.toLowerCase()) {
        case 'on time': return 'success';
        case 'delayed': return 'danger';
        case 'approaching': return 'warning';
        case 'at platform': return 'info';
        default: return 'secondary';
    }
}

function getSeverityClass(severity) {
    switch(severity.toLowerCase()) {
        case 'high': return 'danger';
        case 'medium': return 'warning';
        case 'low': return 'info';
        default: return 'secondary';
    }
}