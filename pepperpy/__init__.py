"""PepperPy Framework"""

__version__ = "0.1.0"

# Lazy imports
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .ai import AIClient
    from .console import Console
    from .db import DatabaseConfig

__all__ = [
    "AIClient",
    "Console", 
    "DatabaseConfig",
]
