# pypepper/error.py
from .logging import get_logger

logger = get_logger()


def handle_exception(error, custom_message="An error occurred"):
    """Log an exception with a custom message."""
    logger.error(f"{custom_message}: {error}")


# Example usage
# try:
#     risky_operation()
# except Exception as e:
#     handle_exception(e, "Operation failed")
