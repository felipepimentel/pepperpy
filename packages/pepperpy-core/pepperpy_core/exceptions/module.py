"""Module-related exceptions"""

from .base import PepperPyError


class ModuleError(PepperPyError):
    """Base module error"""


__all__ = [
    "ModuleError",
]
