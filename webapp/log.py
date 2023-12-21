from pydantic import BaseModel

class LogConfig(BaseModel):
    """Logging configuration to be set for the server"""

    LOGGER_NAME: str = "cloud"
    LOG_FORMAT: str = "%(levelprefix)s | %(asctime)s | %(message)s"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        'standard': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%b/%d/%Y %H:%M:%S"
        }
    }
    handlers = {
        "console": {
            "formatter": "standard",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
        "file": {
            "level": 'INFO',
            "class": 'logging.handlers.RotatingFileHandler',
            "formatter": "standard",
            "filename": 'cloud.log',
            'maxBytes': 1024 * 1025 * 50,
            'backupCount': 10,
        }
    }
    loggers = {
        LOGGER_NAME: {"handlers": ["console", "file"], "level": LOG_LEVEL},
    }