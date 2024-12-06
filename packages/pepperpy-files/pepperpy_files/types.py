"""File types module."""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any


@dataclass
class FileMetadata:
    """File metadata."""

    name: str
    mime_type: str
    size: int
    format: str
    additional_metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class FileContent:
    """File content."""

    path: Path
    content: str | bytes
    metadata: FileMetadata
