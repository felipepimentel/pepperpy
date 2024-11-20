"""File handling configuration"""

from dataclasses import dataclass, field
from pathlib import Path

from pepperpy.core.types import JsonDict, ModuleConfig


@dataclass
class FileHandlerConfig(ModuleConfig):
    """File handler configuration"""

    base_path: Path | None = None
    allowed_extensions: list[str] = field(default_factory=list)
    max_size: int | None = None  # in bytes
    chunk_size: int = 8192  # in bytes
    encoding: str = "utf-8"
    create_dirs: bool = True
    overwrite: bool = False
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class FileManagerConfig(ModuleConfig):
    """File manager configuration"""

    handlers: dict[str, FileHandlerConfig] = field(default_factory=dict)
    default_handler: str | None = None
    base_path: Path | None = None
    metadata: JsonDict = field(default_factory=dict)
