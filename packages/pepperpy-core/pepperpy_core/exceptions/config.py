"""Configuration-related exceptions"""

from .base import PepperPyError


class ConfigError(PepperPyError):
    """Base configuration error"""


__all__ = [
    "ConfigError",
]
