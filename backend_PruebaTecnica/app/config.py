import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

class Config:
    """Configuración base"""
    # Flask
    FLASK_APP = os.getenv('FLASK_APP', 'run.py')
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', True)
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # API
    STACK_EXCHANGE_API_URL = os.getenv('STACK_EXCHANGE_API_URL')
    
    # Security
    SECRET_KEY = os.getenv('SECRET_KEY')

class DevelopmentConfig(Config):
    """Configuración de desarrollo"""
    DEBUG = True

class ProductionConfig(Config):
    """Configuración de producción"""
    DEBUG = False

# Diccionario de configuraciones
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}