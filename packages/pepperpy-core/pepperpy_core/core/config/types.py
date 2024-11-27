"""Configuration type definitions"""

from enum import Enum
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field

from ...base.types import JsonDict


class ConfigFormat(str, Enum):
    """Configuration format"""

    JSON = "json"
    YAML = "yaml"
    TOML = "toml"


class ConfigSource(BaseModel):
    """Configuration source"""

    path: Path
    format: ConfigFormat = ConfigFormat.JSON
    required: bool = True
    metadata: JsonDict = Field(default_factory=dict)
    model_config = ConfigDict(frozen=True)


class ConfigManagerConfig(BaseModel):
    """Configuration manager configuration"""

    config_dir: Path = Field(default=Path("config"))
    env_prefix: str = Field(default="PEPPERPY_")
    default_format: ConfigFormat = ConfigFormat.JSON
    sources: list[ConfigSource] = Field(default_factory=list)
    metadata: JsonDict = Field(default_factory=dict)
    model_config = ConfigDict(frozen=True)
