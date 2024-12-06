"""File handling package."""

from .config import FileHandlerConfig, FileManagerConfig
from .exceptions import FileError
from .manager import FileManager
from .types import FileContent, FileMetadata

__all__ = [
    "FileHandlerConfig",
    "FileManagerConfig",
    "FileError",
    "FileManager",
    "FileContent",
    "FileMetadata",
]
