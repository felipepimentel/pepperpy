"""Core configuration module"""

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

from .config import Config, load_config


@dataclass
class ModuleConfig:
    """Base module configuration"""

    name: str
    version: str
    debug: bool = False
    description: Optional[str] = None
    dependencies: Optional[List[str]] = None
    config: Dict[str, Any] = field(default_factory=dict)


__all__ = ["ModuleConfig", "Config", "load_config"]
