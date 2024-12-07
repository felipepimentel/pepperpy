"""File handler configuration."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class FileHandlerConfig:
    """File handler configuration."""

    allowed_extensions: list[str] | set[str]
    path: Path | None = None
    max_size: int = 10 * 1024 * 1024  # 10MB default
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class FileManagerConfig:
    """File manager configuration."""

    base_path: Path
    max_file_size: int = 100 * 1024 * 1024  # 100MB default
    allowed_extensions: set[str] = field(default_factory=set)
