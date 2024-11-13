"""File handling types"""

from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Protocol, runtime_checkable


@runtime_checkable
class PDFDocument(Protocol):
    """Protocol for PDF document"""

    metadata: Dict[str, str]

    def get_toc(self) -> List[Any]: ...
    def get_form_text_fields(self) -> Dict[str, str]: ...
    def new_page(self) -> "PDFPage": ...
    def set_metadata(self, metadata: Dict[str, Any]) -> None: ...
    def save(self, path: str, **kwargs: Any) -> None: ...
    def close(self) -> None: ...
    def extract_image(self, xref: int) -> Dict[str, Any]: ...
    def __iter__(self) -> Any: ...  # Para suportar iteração sobre páginas


@runtime_checkable
class PDFPage(Protocol):
    """Protocol for PDF page"""

    parent: PDFDocument

    def get_text(self) -> str: ...
    def get_links(self) -> List[Dict[str, Any]]: ...
    def get_images(self) -> List[Any]: ...
    def insert_text(self, point: tuple[float, float], text: str) -> None: ...
    def insert_image(self, rect: Any, stream: bytes) -> None: ...


@dataclass
class MediaInfo:
    type: Literal["image", "video", "audio"]
    width: Optional[int] = None
    height: Optional[int] = None
    format: Optional[str] = None
    mode: Optional[str] = None
    channels: Optional[int] = None
    duration: Optional[float] = None
    fps: Optional[float] = None
    total_frames: Optional[int] = None
    sample_width: Optional[int] = None
    frame_rate: Optional[int] = None


@dataclass
class FileContent:
    content: Any
    metadata: Dict[str, Any]
    format: str


@dataclass
class SpreadsheetStats:
    row_count: int
    column_count: int
    missing_values: Dict[str, int]
    column_types: Dict[str, Any]
    numeric_stats: Dict[str, Dict[str, float]]
    memory_usage: int
    duplicates: int


@dataclass
class FileMetadata:
    """File metadata"""

    path: Path
    size: int
    created_at: datetime
    modified_at: datetime
    mime_type: Optional[str] = None
    encoding: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Chapter:
    """E-book chapter"""

    title: str
    content: str
    order: int
    level: int = 1
    identifier: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EpubTOC:
    """E-book table of contents"""

    items: List[Chapter]
    max_depth: int = 3


@dataclass
class ImageInfo:
    """Image information"""

    width: int
    height: int
    mode: str
    format: str
    channels: Optional[int] = None
    bits: Optional[int] = None
    dpi: Optional[tuple[float, float]] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AudioInfo:
    """Audio file information"""

    duration: float
    sample_rate: int
    channels: int
    format: str
    bit_depth: Optional[int] = None
    bitrate: Optional[int] = None
    codec: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class FileStats:
    """File statistics"""

    name: str
    extension: str
    size: int
    created_at: datetime
    modified_at: datetime
    hash: str
    metadata: Dict[str, Any] = field(default_factory=dict)
