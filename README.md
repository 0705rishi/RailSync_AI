# RAILSYNC-AI

RailSync-AI is a Railway Traffic Control System built using Flask that simulates and optimizes train scheduling and conflict detection through AI algorithms like genetic optimization.

## Features

- Real-time dashboard for train status monitoring.
- Detects potential train conflicts for safe scheduling.
- Optimizes train schedules using a genetic algorithm.
- Simulates "what-if" scenarios for railway traffic control.
- Provides system performance metrics for evaluation.

## Setup Instructions

1. Clone the repository:
2. Create and activate a Python virtual environment:
3. Install the dependencies:text

## Running the Application

Start the Flask application by running:
python run.py

By default, the server will start on `0.0.0.0:5000`.

## Project Structure

- `app.py` - Contains the Flask app with routes for the dashboard, API endpoints for trains, conflict detection, schedule optimization, scenario simulation, and metrics.
- `config.py` - Configuration for the Flask app settings and AI model parameters.
- `run.py` - Entry point script to launch the Flask application.
- `requirements.txt` - Lists required Python packages.

## Dependencies

The project depends on:
- Flask 2.3.3
- Werkzeug 2.3.7
- numpy 1.24.3
- requests 2.31.0
- python-dateutil 2.8.2
- gunicorn 21.2.0
- python-dotenv 1.0.0
- flask-cors 4.0.0

These are automatically installed using the `requirements.txt`.

## License

This project is released under the MIT License.


Feel free to contribute and raise issues for improvements or bug fixes.
