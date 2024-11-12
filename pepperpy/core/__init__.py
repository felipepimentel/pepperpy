"""Core module providing shared functionality across PepperPy"""

from .config import ModuleConfig
from .exceptions import CoreError
from .module import BaseModule, ModuleMetadata
from .types import JsonDict

__all__ = ["BaseModule", "ModuleMetadata", "ModuleConfig", "JsonDict", "CoreError"]
