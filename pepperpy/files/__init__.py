"""File handling module"""

from .config import FileManagerConfig
from .exceptions import FileError
from .handlers.base import BaseFileHandler, FileHandler
from .manager import FileManager
from .types import (
    Book,
    BookMetadata,
    Chapter,
    FileContent,
    FileMetadata,
    FileType,
    ImageInfo,
    MediaInfo,
    PathLike,
    ensure_path,
)

__all__ = [
    # Core
    "FileManager",
    "FileManagerConfig",
    # Handlers
    "FileHandler",
    "BaseFileHandler",
    # Types
    "Book",
    "BookMetadata",
    "Chapter",
    "FileContent",
    "FileMetadata",
    "FileType",
    "ImageInfo",
    "MediaInfo",
    "PathLike",
    # Utils
    "ensure_path",
    # Exceptions
    "FileError",
]
