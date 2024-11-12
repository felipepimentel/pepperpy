"""Configuration type definitions"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Optional

from pepperpy.core.types import JsonDict


class ConfigFormat(Enum):
    """Configuration file formats"""

    YAML = "yaml"
    JSON = "json"
    TOML = "toml"
    INI = "ini"


@dataclass
class ConfigSource:
    """Configuration source information"""

    name: str
    path: Optional[Path] = None
    format: Optional[ConfigFormat] = None
    last_modified: Optional[datetime] = None
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class ConfigValue:
    """Configuration value with metadata"""

    value: Any
    source: ConfigSource
    updated_at: datetime = field(default_factory=datetime.utcnow)
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class ConfigSnapshot:
    """Configuration state snapshot"""

    values: Dict[str, ConfigValue]
    created_at: datetime = field(default_factory=datetime.utcnow)
    metadata: JsonDict = field(default_factory=dict)
