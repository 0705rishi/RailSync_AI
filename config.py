import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'railsync-ai-sih2025-secret'
    
    # Database configuration (for future use)
    DATABASE_URL = os.environ.get('DATABASE_URL') or 'sqlite:///railsync.db'
    
    # AI Model parameters
    GA_POPULATION_SIZE = int(os.environ.get('GA_POPULATION_SIZE') or 50)
    GA_GENERATIONS = int(os.environ.get('GA_GENERATIONS') or 30)
    GA_MUTATION_RATE = float(os.environ.get('GA_MUTATION_RATE') or 0.1)
    
    # System parameters
    SAFETY_BUFFER_MINUTES = int(os.environ.get('SAFETY_BUFFER_MINUTES') or 5)
    CONFLICT_DISTANCE_THRESHOLD = int(os.environ.get('CONFLICT_DISTANCE_THRESHOLD') or 2)  # km
    MAX_TRAIN_SPEED = int(os.environ.get('MAX_TRAIN_SPEED') or 160)  # km/h
    
    # API settings
    API_RATE_LIMIT = int(os.environ.get('API_RATE_LIMIT') or 100)  # requests per minute
    REAL_TIME_UPDATE_INTERVAL = int(os.environ.get('REAL_TIME_UPDATE_INTERVAL') or 30)  # seconds
    
    # Flask settings
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    HOST = os.environ.get('FLASK_HOST') or '0.0.0.0'
    PORT = int(os.environ.get('FLASK_PORT') or 5000)
    
    # Railway specific settings
    DEFAULT_PLATFORM_COUNT = 4
    DEFAULT_TRACK_CAPACITY = 2
    MAX_DELAY_MINUTES = 120
    MIN_TRAIN_SPEED = 40
    
    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    
class TestingConfig(Config):
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
