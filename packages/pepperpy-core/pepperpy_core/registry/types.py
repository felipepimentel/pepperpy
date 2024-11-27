"""Registry type definitions"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, Type


@dataclass
class Registration:
    """Component registration data"""

    name: str
    component_type: Type[Any]
    factory: Callable[..., Any]
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RegistryEntry:
    """Registry entry data"""

    name: str
    component_type: Type[Any]
    factory: Callable[..., Any]
    metadata: Dict[str, Any] = field(default_factory=dict)
