"""File handling configuration"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Set

from pepperpy.core.config import ModuleConfig


@dataclass
class FileConfig(ModuleConfig):
    """Configuration for file operations"""

    default_encoding: str = "utf-8"
    chunk_size: int = 8192
    max_file_size: Optional[int] = None
    allowed_extensions: Optional[Set[str]] = None
    create_dirs: bool = True
    backup_enabled: bool = False
    backup_dir: Optional[str] = None
    metadata_enabled: bool = True
    params: Dict[str, Any] = field(default_factory=dict)
