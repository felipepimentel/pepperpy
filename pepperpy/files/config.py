"""File handling configuration"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, ClassVar

from pepperpy.core.types import JsonDict, ModuleConfig


@dataclass
class FileManagerConfig(ModuleConfig):
    """File manager configuration"""

    name: str = "file_manager"
    base_path: Path | None = None
    handlers: dict[str, Any] = field(default_factory=dict)
    metadata: JsonDict = field(default_factory=dict)
    _instance: ClassVar[Any] = None

    @classmethod
    def get_default(cls) -> "FileManagerConfig":
        """Get default configuration instance"""
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
