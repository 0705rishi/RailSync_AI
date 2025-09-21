"""
RailSync AI Models Package

This package contains all the data models and AI components for the railway traffic control system.
"""

from .data_models import Train, Station, TrackSection
from .genetic_optimizer import GeneticOptimizer
from .conflict_detector import ConflictDetector

__version__ = '1.0.0'
__author__ = 'SIH 2025 Team'

# Package-level exports
__all__ = [
    'Train',
    'Station', 
    'TrackSection',
    'GeneticOptimizer',
    'ConflictDetector'
]

# Model registry for easy access
MODEL_REGISTRY = {
    'train': Train,
    'station': Station,
    'track_section': TrackSection
}

# AI Component registry
AI_COMPONENTS = {
    'optimizer': GeneticOptimizer,
    'detector': ConflictDetector
}

def get_model(model_name):
    """Get model class by name"""
    return MODEL_REGISTRY.get(model_name.lower())

def get_ai_component(component_name):
    """Get AI component class by name"""
    return AI_COMPONENTS.get(component_name.lower())

def create_optimizer(**kwargs):
    """Factory function to create genetic optimizer"""
    return GeneticOptimizer(**kwargs)

def create_detector(**kwargs):
    """Factory function to create conflict detector"""
    return ConflictDetector(**kwargs)

# Initialize logging for models
import logging
logging.getLogger(__name__).addHandler(logging.NullHandler())
