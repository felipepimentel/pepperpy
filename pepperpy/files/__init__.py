"""File handling module"""

from .handlers.audio import AudioHandler
from .handlers.base import FileHandler
from .handlers.compression import CompressionHandler
from .handlers.config import ConfigHandler
from .handlers.document import DocumentHandler
from .handlers.epub import EPUBHandler
from .handlers.image import ImageHandler
from .handlers.markdown import MarkdownHandler
from .handlers.markdown_enhanced import MarkdownEnhancedHandler
from .handlers.media import MediaHandler
from .manager import FileManager
from .types import (
    FileContent,
    FileMetadata,
    FileType,
    ImageInfo,
    MediaInfo,
    PathLike,
    ensure_path,
)

__all__ = [
    "AudioHandler",
    "FileHandler",
    "CompressionHandler",
    "ConfigHandler",
    "DocumentHandler",
    "EPUBHandler",
    "ImageHandler",
    "MarkdownHandler",
    "MarkdownEnhancedHandler",
    "MediaHandler",
    "FileManager",
    "FileContent",
    "FileMetadata",
    "FileType",
    "ImageInfo",
    "MediaInfo",
    "PathLike",
    "ensure_path",
]
