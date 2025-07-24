import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-please-change-in-production'
    DEBUG = False
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # JWT configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-dev-key-please-change'
    JWT_ACCESS_TOKEN_EXPIRES = 60 * 60 * 24  # 24 hours
    
    # Email configuration
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'True').lower() in ['true', 'yes', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    DEBUG_EMAIL = os.environ.get('DEBUG_EMAIL', 'False').lower() in ['true', 'yes', '1']

class DevelopmentConfig(Config):
    DEBUG = True
    
class ProductionConfig(Config):
    DEBUG = False
    
    # In production, ensure all security settings are properly configured
    # and environment variables are set
    def __init__(self):
        if not os.environ.get('SECRET_KEY'):
            raise ValueError("SECRET_KEY environment variable is not set")
        if not os.environ.get('JWT_SECRET_KEY'):
            raise ValueError("JWT_SECRET_KEY environment variable is not set")
        if not os.environ.get('DATABASE_URL'):
            raise ValueError("DATABASE_URL environment variable is not set")

# Export configuration based on environment
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config():
    flask_env = os.environ.get('FLASK_ENV', 'default')
    return config.get(flask_env, config['default'])()
