"""File type definitions"""

from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class FileType(str, Enum):
    """File type enumeration"""

    DOCUMENT = "document"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    ARCHIVE = "archive"
    CONFIG = "config"
    DATA = "data"
    TEXT = "text"
    BINARY = "binary"
    JSON = "json"
    YAML = "yaml"
    MARKUP = "markup"
    SPREADSHEET = "spreadsheet"
    MEDIA = "media"
    OTHER = "other"


@dataclass
class FileMetadata:
    """File metadata"""

    path: str
    name: str
    extension: str
    type: str
    mime_type: str
    format: str
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime | None = None
    size: int = 0
    extra: dict[str, Any] = field(default_factory=dict)


@dataclass
class ImageInfo:
    """Image information"""

    width: int
    height: int
    channels: int
    mode: str
    format: str

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class MediaInfo:
    """Media information"""

    duration: float
    bitrate: int
    codec: str
    format: str
    channels: int = 2
    sample_rate: int = 44100

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary"""
        return asdict(self)


@dataclass
class Chapter:
    """Book chapter"""

    title: str
    content: str
    order: int
    file_name: str
    level: int = 0
    images: dict[str, bytes] = field(default_factory=dict)


@dataclass
class BookMetadata:
    """Book metadata"""

    title: str
    authors: list[str]
    language: str = "en"
    identifier: str | None = None
    publisher: str | None = None
    publication_date: datetime | None = None
    description: str | None = None
    subjects: list[str] = field(default_factory=list)
    rights: str | None = None


@dataclass
class Book:
    """Book content"""

    metadata: BookMetadata
    chapters: list[Chapter]
    toc: list[tuple[Any, ...]] = field(default_factory=list)
    cover_image: bytes | None = None
    images: dict[str, bytes] = field(default_factory=dict)
    styles: dict[str, str] = field(default_factory=dict)
    resources: dict[str, bytes] = field(default_factory=dict)


@dataclass
class FileContent(Generic[T]):
    """File content with metadata"""

    content: T
    metadata: FileMetadata


def ensure_path(path: Path | str) -> Path:
    """Ensure path is a Path object"""
    return path if isinstance(path, Path) else Path(path)


PathLike = Path | str
