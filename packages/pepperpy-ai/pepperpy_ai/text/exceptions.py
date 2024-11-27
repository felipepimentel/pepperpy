"""Text analysis exceptions"""

from typing import Optional

from bko.core.exceptions import CoreError


class TextError(CoreError):
    """Base exception for text errors"""

    pass


class TextAnalysisError(TextError):
    """Base exception for text analysis errors"""

    def __init__(self, message: str, cause: Optional[Exception] = None) -> None:
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
