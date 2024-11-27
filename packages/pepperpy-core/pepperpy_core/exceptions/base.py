"""Base exceptions"""

from typing import Any, Optional


class PepperPyError(Exception):
    """Base exception for all framework errors"""

    def __init__(self, message: str, cause: Optional[Exception] = None, **metadata: Any) -> None:
        super().__init__(message)
        self.cause = cause
        self.metadata = metadata

    def __str__(self) -> str:
        if self.cause:
            return f"{super().__str__()} (caused by: {self.cause})"
        return super().__str__()


class ValidationError(PepperPyError):
    """Validation error"""


__all__ = [
    "PepperPyError",
    "ValidationError",
]
