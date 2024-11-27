"""File configuration"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Set

from pydantic import BaseModel


@dataclass
class FileHandlerConfig(BaseModel):
    """File handler configuration"""

    base_path: Path
    allowed_extensions: Set[str]
    max_file_size: int
    metadata: Dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        """Validate configuration"""
        if not self.base_path:
            raise ValueError("Base path cannot be empty")
        if not self.allowed_extensions:
            raise ValueError("Allowed extensions cannot be empty")
        if self.max_file_size <= 0:
            raise ValueError("Max file size must be positive")


@dataclass
class FileManagerConfig(FileHandlerConfig):
    """File manager configuration"""

    def __post_init__(self) -> None:
        """Validate configuration"""
        super().__post_init__()

        # Additional manager-specific validation
        if not any(ext.startswith(".") for ext in self.allowed_extensions):
            raise ValueError("Extensions must start with '.'")
