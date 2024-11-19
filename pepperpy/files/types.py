"""File handling types and constants"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from pathlib import Path
from typing import Any, Generic, TypeVar, Union

try:
    from pypdf._page import PageObject  # Updated import path
except ImportError:
    # Fallback type alias for when pypdf is not installed
    PageObject = Any

T = TypeVar("T")

# Type alias for PDF pages
PDFPage = PageObject


class FileType(Enum):
    """File type enumeration"""

    TEXT = auto()
    BINARY = auto()
    IMAGE = auto()
    AUDIO = auto()
    VIDEO = auto()
    MEDIA = auto()
    PDF = auto()
    DOCUMENT = auto()
    SPREADSHEET = auto()
    JSON = auto()
    YAML = auto()
    CONFIG = auto()
    MARKDOWN = auto()
    HTML = auto()
    XML = auto()
    EPUB = auto()
    COMPRESSED = auto()
    MARKUP = auto()


PathLike = Union[str, Path]


def ensure_path(path: PathLike) -> Path:
    """Ensure path is a Path object."""
    return Path(path) if not isinstance(path, Path) else path


@dataclass
class MediaInfo:
    """Media file information"""

    duration: float
    bitrate: int
    codec: str
    format: str = ""
    channels: int = 0
    sample_rate: int = 0
    frame_rate: float = 0.0


@dataclass
class FileMetadata:
    """File metadata"""

    name: str
    size: int
    file_type: FileType
    mime_type: str
    format: str
    created_at: datetime
    modified_at: datetime
    path: Path
    metadata: dict[str, Any] = field(default_factory=dict)
    media_info: MediaInfo | None = None
    image_info: Any = None


@dataclass
class FileContent(Generic[T]):
    """File content with metadata"""

    content: T
    metadata: FileMetadata


@dataclass
class ImageInfo:
    """Image file information"""

    width: int
    height: int
    format: str
    mode: str
    channels: int = 0
    bits: int = 0
    dpi: tuple[float, float] | None = None


@dataclass
class BookMetadata:
    """Book metadata"""

    title: str
    authors: list[str]
    language: str
    identifier: str
    description: str | None = None
    publisher: str | None = None
    rights: str | None = None
    publication_date: datetime | None = None
    subjects: list[str] = field(default_factory=list)


@dataclass
class Chapter:
    """Book chapter"""

    title: str
    content: str
    file_name: str
    order: int = 0
    level: int = 0


@dataclass
class Book:
    """Book content"""

    metadata: BookMetadata
    chapters: list[Chapter]
    cover_image: bytes | None = None
    styles: dict[str, str] = field(default_factory=dict)
    images: dict[str, bytes] = field(default_factory=dict)
    resources: dict[str, bytes] = field(default_factory=dict)
    toc: list[tuple[Any, ...]] = field(default_factory=list)
