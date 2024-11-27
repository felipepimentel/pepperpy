"""Core exceptions base module"""

from typing import Optional


class CoreError(Exception):
    """Base exception for all core errors"""

    def __init__(self, message: str, cause: Optional[Exception] = None) -> None:
        """Initialize error"""
        super().__init__(message)
        self._message = message
        self._cause = cause

    @property
    def message(self) -> str:
        """Get error message"""
        return self._message

    @property
    def cause(self) -> Optional[Exception]:
        """Get original exception"""
        return self._cause


class PepperPyError(Exception):
    """Base exception for all PepperPy errors"""

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause


class ModuleError(PepperPyError):
    """Base exception for module-related errors"""


class ResourceError(PepperPyError):
    """Base exception for resource-related errors"""


class ConfigError(PepperPyError):
    """Base exception for configuration-related errors"""
