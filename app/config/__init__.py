""" Configuration for app environment """

from os import environ, path
from typing import Final

from dotenv import load_dotenv

from app.config.llm_config import LLMConfig, OpenAIConfig

basedir = path.abspath(path.join(path.dirname(__file__), '../../'))

# loading env vars from .env file
load_dotenv()

class BaseConfig(object):
    """ Base config class. """

    # FastAPI app
    APP_VERSION: Final = "0.1.0"
    APP_NAME: Final = environ.get('APP_NAME') or 'LangChain LLM classifications demo'
    APP_DESCRIPTION: Final = "Description of technical interview"

    # LLM configuration
    LLM: LLMConfig = OpenAIConfig()

    # Logging
    LOG_INFO_FILE: str = path.join(basedir, 'logs', 'info.log')
    LOGGING: dict = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'standard': {
                'format': '[%(asctime)s] - %(name)s - %(levelname)s - %(message)s',
                'datefmt': '%b %d %Y %H:%M:%S'
            },
            'simple': {
                'format': '%(levelname)s - %(message)s'
            },
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',  # Add StreamHandler for console output, this is important for Docker
                'formatter': 'simple'
            },
            'log_info_file': {
                'level': 'INFO',
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': LOG_INFO_FILE,
                'maxBytes': 16777216,  # 16 megabytes
                'formatter': 'standard',
                'backupCount': 5
            },
        },
        'loggers': {
            APP_NAME: {
                'level': 'DEBUG',
                'handlers': ['console', 'log_info_file'],  # Add console handler
            },
        },
    }

    # Middleware
    CORS_ORIGINS:list = [
        '*',
    ]
    ALLOWED_METHODS:list = [
        '*',
    ]
    ALLOWED_HEADERS:list = [
        '*',
    ]

class Development(BaseConfig):
    """ Development config. """
    DEBUG = True
    TESTING = False
    ENV = 'dev'

class Testing(BaseConfig):
    """ Testing config. """
    DEBUG = True
    TESTING = True
    ENV = 'testing'

class Production(BaseConfig):
    """ Production config """
    DEBUG = False
    TESTING = False
    ENV = 'production'

config = {
    'development': Development,
    'testing': Testing,
    'production': Production,
}
