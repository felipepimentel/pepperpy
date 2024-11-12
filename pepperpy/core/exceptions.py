"""Core exceptions"""


class CoreError(Exception):
    """Base exception for core errors"""

    def __init__(self, message: str, cause: Exception = None):
        super().__init__(message)
        self.cause = cause
