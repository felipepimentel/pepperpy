"""Core exceptions module"""

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