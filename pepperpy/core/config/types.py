"""Configuration type definitions"""

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, Union

from pepperpy.core.types import JsonDict


class ConfigFormat(str, Enum):
    """Configuration format"""

    JSON = "json"
    YAML = "yaml"
    TOML = "toml"
    ENV = "env"
    INI = "ini"


ConfigValue = Union[str, int, float, bool, list[Any], dict[str, Any], None]


@dataclass
class ConfigSource:
    """Configuration source"""

    name: str
    path: Path | None = None
    format: ConfigFormat | None = None
    data: dict[str, ConfigValue] = field(default_factory=dict)
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class ConfigManagerConfig:
    """Configuration manager configuration"""

    name: str
    sources: list[ConfigSource] = field(default_factory=list)
    auto_load: bool = True
    metadata: JsonDict = field(default_factory=dict)
