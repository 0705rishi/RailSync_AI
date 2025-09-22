// RailSync AI Dashboard JavaScript with Mumbai Metro Animation

let refreshInterval;
let animationRunning = false;
let trains = [];

// Initialize dashboard when page loads
document.addEventListener('DOMContentLoaded', function() {
    loadMetrics();
    loadTrains();
    detectConflicts();
    initializeMumbaiMetroMap();
    
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
        
        document.getElementById('total-trains').textContent = metrics.total_trains || 0;
        document.getElementById('active-conflicts').textContent = metrics.active_conflicts || 0;
        document.getElementById('average-delay').textContent = `${(metrics.average_delay || 0).toFixed(1)}min`;
        document.getElementById('system-efficiency').textContent = `${metrics.system_efficiency || 0}%`;
        document.getElementById('throughput-today').textContent = metrics.throughput_today || 0;
        document.getElementById('ai-success-rate').textContent = `${metrics.optimization_success_rate || 0}%`;
        
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
                            <small class="text-muted">${train.current_position} â†’ ${train.destination}</small>
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

// Mumbai Metro Map Implementation
let svg, metroLines, metroStations;

function initializeMumbaiMetroMap() {
    setTimeout(() => {
        try {
            svg = d3.select('#mumbai-metro-map');
            svg.selectAll('*').remove();

            // Define Mumbai Metro Lines with realistic coordinates
            metroLines = [
                {
                    id: 'line1',
                    name: 'Line 1 (Red)',
                    color: '#d43f3a',
                    width: 12,
                    stations: [
                        { name: 'Andheri', x: 120, y: 80 },
                        { name: 'Ville Parle', x: 150, y: 95 },
                        { name: 'Santacruz', x: 180, y: 110 },
                        { name: 'Bandra', x: 210, y: 125 },
                        { name: 'Mahim', x: 240, y: 140 },
                        { name: 'Dadar', x: 270, y: 155 },
                    ]
                },
                {
                    id: 'line2',
                    name: 'Line 2 (Orange)',
                    color: '#ff6600',
                    width: 12,
                    stations: [
                        { name: 'Dadar', x: 270, y: 155 },
                        { name: 'Parel', x: 320, y: 140 },
                        { name: 'Matunga Road', x: 370, y: 125 },
                        { name: 'Kurla', x: 420, y: 180 },
                        { name: 'Ghatkopar', x: 500, y: 200 },
                        { name: 'Mulund', x: 580, y: 160 },
                        { name: 'Nahur', x: 620, y: 140 },
                        { name: 'Bhandup', x: 660, y: 120 },
                        { name: 'Vikhroli', x: 700, y: 100 },
                        { name: 'Kanjur Marg', x: 740, y: 120 },
                        { name: 'Thane', x: 850, y: 110 }
                    ]
                },
                {
                    id: 'line3',
                    name: 'Line 3 (Green)',
                    color: '#28a745',
                    width: 10,
                    stations: [
                        { name: 'Kurla', x: 420, y: 180 },
                        { name: 'Sion', x: 400, y: 250 },
                        { name: 'Chunabhatti', x: 380, y: 320 },
                        { name: 'GTB Nagar', x: 360, y: 390 },
                        { name: 'Wadala Rd.', x: 340, y: 460 },
                        { name: 'Sewri', x: 420, y: 480 },
                        { name: 'Cotton Green', x: 500, y: 500 },
                        { name: 'Reay Road', x: 580, y: 480 },
                        { name: 'Dockyard Road', x: 660, y: 460 },
                        { name: 'Masjid', x: 740, y: 440 },
                        { name: 'CSMT', x: 800, y: 420 }
                    ]
                }
            ];

            // Combine all stations for easy access
            metroStations = [];
            metroLines.forEach(line => {
                line.stations.forEach(station => {
                    if (!metroStations.find(s => s.name === station.name)) {
                        metroStations.push({...station, lines: [line.id]});
                    } else {
                        const existingStation = metroStations.find(s => s.name === station.name);
                        existingStation.lines.push(line.id);
                        existingStation.interchange = true;
                    }
                });
            });

            drawMetroLines();
            drawMetroStations();
            drawTimeDistanceLabels();
            
            // Initialize trains
            trains = [
                { id: 'T001', name: 'Express 1', lineId: 'line1', position: 0, direction: 1, speed: 2 },
                { id: 'T002', name: 'Local 2', lineId: 'line2', position: 0.3, direction: 1, speed: 1.5 },
                { id: 'T003', name: 'Express 3', lineId: 'line3', position: 0.7, direction: -1, speed: 2.2 },
                { id: 'T004', name: 'Local 4', lineId: 'line1', position: 0.8, direction: -1, speed: 1.8 }
            ];

            drawTrains();
            console.log('Mumbai Metro map initialized successfully');

        } catch (error) {
            console.error('Error initializing metro map:', error);
        }
    }, 1000);
}

function drawMetroLines() {
    metroLines.forEach(line => {
        const lineData = line.stations;
        
        // Create smooth curved path
        const lineGenerator = d3.line()
            .x(d => d.x)
            .y(d => d.y)
            .curve(d3.curveBasis);

        svg.append('path')
            .datum(lineData)
            .attr('d', lineGenerator)
            .attr('fill', 'none')
            .attr('stroke', line.color)
            .attr('stroke-width', line.width)
            .attr('stroke-linecap', 'round')
            .attr('id', `path-${line.id}`);
    });
}

function drawMetroStations() {
    metroStations.forEach(station => {
        // Station circle
        svg.append('circle')
            .attr('cx', station.x)
            .attr('cy', station.y)
            .attr('r', station.interchange ? 15 : 10)
            .attr('fill', station.interchange ? '#ffc107' : '#ffffff')
            .attr('stroke', '#000000')
            .attr('stroke-width', station.interchange ? 4 : 3)
            .style('cursor', 'pointer')
            .on('mouseover', function() {
                d3.select(this).attr('r', (station.interchange ? 18 : 13));
            })
            .on('mouseout', function() {
                d3.select(this).attr('r', (station.interchange ? 15 : 10));
            });

        // Station name
        svg.append('text')
            .attr('x', station.x + 20)
            .attr('y', station.y + 6)
            .text(station.name)
            .attr('font-size', station.interchange ? '14px' : '12px')
            .attr('font-weight', station.interchange ? 'bold' : 'normal')
            .attr('fill', '#000000');
    });
}

function drawTimeDistanceLabels() {
    metroStations.forEach((station, index) => {
        if (index % 2 === 0) { // Show labels for alternate stations to avoid clutter
            // Time/Distance info box
            svg.append('rect')
                .attr('x', station.x - 25)
                .attr('y', station.y - 35)
                .attr('width', 50)
                .attr('height', 20)
                .attr('fill', '#ffe066')
                .attr('stroke', '#d4a00f')
                .attr('stroke-width', 1)
                .attr('rx', 6);

            svg.append('text')
                .attr('x', station.x)
                .attr('y', station.y - 21)
                .text(`${Math.floor(Math.random() * 8) + 5}|${Math.floor(Math.random() * 15) + 10}`)
                .attr('font-size', '10px')
                .attr('fill', '#333')
                .attr('text-anchor', 'middle');
        }
    });
}

function drawTrains() {
    const trainElements = svg.selectAll('circle.metro-train')
        .data(trains, d => d.id);

    // Enter new trains
    trainElements.enter()
        .append('circle')
        .attr('class', 'metro-train')
        .attr('r', 8)
        .attr('fill', '#007bff')
        .attr('stroke', '#ffffff')
        .attr('stroke-width', 2)
        .style('cursor', 'pointer')
        .append('title')
        .text(d => `${d.name} - Line ${d.lineId}`);

    // Update train positions
    updateTrainPositions();
}

function updateTrainPositions() {
    trains.forEach(train => {
        const line = metroLines.find(l => l.id === train.lineId);
        if (!line) return;

        const stations = line.stations;
        const totalStations = stations.length - 1;
        
        // Calculate position along the line
        let stationIndex = Math.floor(train.position * totalStations);
        let progress = (train.position * totalStations) - stationIndex;
        
        // Handle direction
        if (train.direction === -1) {
            stationIndex = totalStations - stationIndex - 1;
            progress = 1 - progress;
        }
        
        // Interpolate position between stations
        if (stationIndex >= 0 && stationIndex < totalStations) {
            const currentStation = stations[stationIndex];
            const nextStation = stations[stationIndex + 1];
            
            const x = currentStation.x + (nextStation.x - currentStation.x) * progress;
            const y = currentStation.y + (nextStation.y - currentStation.y) * progress;
            
            // Update train position
            svg.select(`circle.metro-train[data-id="${train.id}"]`)
                .attr('cx', x)
                .attr('cy', y);
        }
    });

    // Update train circles with proper data binding
    svg.selectAll('circle.metro-train')
        .attr('cx', d => {
            const line = metroLines.find(l => l.id === d.lineId);
            if (!line) return 0;
            
            const stations = line.stations;
            const totalStations = stations.length - 1;
            let stationIndex = Math.floor(d.position * totalStations);
            let progress = (d.position * totalStations) - stationIndex;
            
            if (d.direction === -1) {
                stationIndex = totalStations - stationIndex - 1;
                progress = 1 - progress;
            }
            
            if (stationIndex >= 0 && stationIndex < totalStations) {
                const currentStation = stations[stationIndex];
                const nextStation = stations[stationIndex + 1];
                return currentStation.x + (nextStation.x - currentStation.x) * progress;
            }
            return 0;
        })
        .attr('cy', d => {
            const line = metroLines.find(l => l.id === d.lineId);
            if (!line) return 0;
            
            const stations = line.stations;
            const totalStations = stations.length - 1;
            let stationIndex = Math.floor(d.position * totalStations);
            let progress = (d.position * totalStations) - stationIndex;
            
            if (d.direction === -1) {
                stationIndex = totalStations - stationIndex - 1;
                progress = 1 - progress;
            }
            
            if (stationIndex >= 0 && stationIndex < totalStations) {
                const currentStation = stations[stationIndex];
                const nextStation = stations[stationIndex + 1];
                return currentStation.y + (nextStation.y - currentStation.y) * progress;
            }
            return 0;
        });
}

function animateTrains() {
    if (!animationRunning) return;

    trains.forEach(train => {
        train.position += (train.speed * 0.001) * train.direction;
        
        // Reverse direction at ends
        if (train.position >= 1 && train.direction === 1) {
            train.direction = -1;
            train.position = 1;
        } else if (train.position <= 0 && train.direction === -1) {
            train.direction = 1;
            train.position = 0;
        }
    });

    updateTrainPositions();
    
    if (animationRunning) {
        requestAnimationFrame(animateTrains);
    }
}

function startAnimation() {
    animationRunning = true;
    animateTrains();
}

function stopAnimation() {
    animationRunning = false;
}

function refreshMetroMap() {
    // Simulate new train positions
    trains.forEach(train => {
        train.position = Math.random();
        train.direction = Math.random() > 0.5 ? 1 : -1;
    });
    updateTrainPositions();
}

// Refresh functions
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