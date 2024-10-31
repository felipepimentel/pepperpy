from loguru import logger
import sys
import os

def setup_logger(log_file="app.log"):
    """Configure loguru logger with console and file outputs."""
    
    # Remove default handler
    logger.remove()
    
    # Configure format for both console and file
    log_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    # Add console handler with colored output
    logger.add(
        sys.stderr,
        format=log_format,
        level="INFO",
        colorize=True
    )

    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Add rotating file handler
    logger.add(
        f"logs/{log_file}",
        format=log_format,
        level="DEBUG",
        rotation="10 MB",
        retention="30 days",
        compression="zip"
    )

def get_logger():
    """Get the configured logger instance."""
    return logger

# Configure logger when module is imported
setup_logger()

# Example usage:
# from .logging import get_logger
# logger = get_logger()
# logger.debug("Debug message")
# logger.info("Info message")
# logger.warning("Warning message")
# logger.error("Error message")
# logger.critical("Critical message") 