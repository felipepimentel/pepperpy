"""Codebase provider types"""

from enum import Enum, auto


class ProviderType(Enum):
    """Provider type enumeration"""

    STATIC = auto()
    DYNAMIC = auto()
    HYBRID = auto() 