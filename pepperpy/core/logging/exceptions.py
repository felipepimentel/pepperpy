"""Logging specific exceptions"""

from pepperpy.core.exceptions import CoreError


class LoggingError(CoreError):
    """Base exception for logging errors"""

    pass


class HandlerError(LoggingError):
    """Error in log handler operation"""

    pass


class FormatterError(LoggingError):
    """Error in log formatting"""

    pass
