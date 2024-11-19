"""Logging-related exceptions"""

from pepperpy.core.exceptions import PepperPyError


class LogError(PepperPyError):
    """Base logging error"""


class LogHandlerError(LogError):
    """Log handler error"""


class LogFormatterError(LogError):
    """Log formatter error"""


class LogConfigError(LogError):
    """Log configuration error"""
