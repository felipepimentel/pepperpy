"""Base exceptions for PepperPy"""


class PepperPyError(Exception):
    """Base exception for all PepperPy errors"""

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause


class ModuleError(PepperPyError):
    """Base exception for module-related errors"""


class ResourceError(PepperPyError):
    """Base exception for resource-related errors""" 