# pypepper/logging.py
from loguru import logger

# Set a default logging configuration
logger.add("logs/pypepper.log", rotation="500 MB")


def get_logger():
    """Return the configured logger instance for the application."""
    return logger
