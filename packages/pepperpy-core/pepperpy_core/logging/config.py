"""Logging configuration"""

from pathlib import Path
from typing import Optional, Sequence

from pydantic import BaseModel, ConfigDict, Field

from ..base.types import JsonDict


class LogHandlerConfig(BaseModel):
    """Log handler configuration"""

    type: str = Field(default="console")
    level: str = Field(default="INFO")
    format: str = Field(default="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    metadata: JsonDict = Field(default_factory=dict)
    model_config = ConfigDict(frozen=True)


class LogConfig(BaseModel):
    """Logging configuration"""

    level: str = Field(default="INFO")
    handlers: Sequence[LogHandlerConfig] = Field(default_factory=list)
    log_dir: Optional[Path] = None
    file_name: Optional[str] = None
    max_bytes: int = Field(default=10 * 1024 * 1024)  # 10MB
    backup_count: int = Field(default=5)
    metadata: JsonDict = Field(default_factory=dict)
    model_config = ConfigDict(frozen=True)
