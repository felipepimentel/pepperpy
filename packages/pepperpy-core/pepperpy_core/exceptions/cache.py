"""Cache-related exceptions"""

from .base import PepperPyError


class CacheError(PepperPyError):
    """Base cache error"""


__all__ = [
    "CacheError",
]
