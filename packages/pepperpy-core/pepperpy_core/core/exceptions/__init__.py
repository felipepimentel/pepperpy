"""Core exceptions package"""

from .base import ConfigError, CoreError, ModuleError, PepperPyError, ResourceError

__all__ = ["CoreError", "PepperPyError", "ModuleError", "ResourceError", "ConfigError"]
