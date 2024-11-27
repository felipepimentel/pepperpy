"""Codebase configuration"""

from pathlib import Path
from typing import Sequence

from pydantic import BaseModel, ConfigDict, Field

from .types import JsonDict


class CodebaseConfig(BaseModel):
    """Codebase configuration"""

    root_path: Path = Field(default=Path.cwd())
    include_patterns: Sequence[str] = Field(default=("**/*.py",))
    exclude_patterns: Sequence[str] = Field(default=("venv/", ".*", "__pycache__/"))
    max_file_size: int = Field(default=1024 * 1024)  # 1MB
    encoding: str = Field(default="utf-8")
    metadata: JsonDict = Field(default_factory=dict)
    model_config = ConfigDict(frozen=True)


class AnalysisConfig(BaseModel):
    """Code analysis configuration"""

    max_depth: int = Field(default=5)
    max_complexity: int = Field(default=10)
    max_line_length: int = Field(default=100)
    ignore_patterns: Sequence[str] = Field(default=tuple())
    metadata: JsonDict = Field(default_factory=dict)
    model_config = ConfigDict(frozen=True)
