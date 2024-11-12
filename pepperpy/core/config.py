"""Core configuration"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class ModuleConfig:
    """Base configuration for modules"""

    name: str
    version: str = "1.0.0"
    description: Optional[str] = None
    enabled: bool = True
    debug: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
