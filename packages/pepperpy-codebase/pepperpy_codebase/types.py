"""Codebase types."""

from collections.abc import Sequence
from dataclasses import dataclass, field
from enum import Enum
from typing import Any

JsonDict = dict[str, Any]


class FileType(str, Enum):
    """File type enumeration."""

    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JSON = "json"
    YAML = "yaml"
    MARKDOWN = "markdown"
    TEXT = "text"
    UNKNOWN = "unknown"


class ChangeType(str, Enum):
    """Change type enumeration."""

    ADDED = "added"
    MODIFIED = "modified"
    DELETED = "deleted"
    RENAMED = "renamed"
    COPIED = "copied"


@dataclass
class FileMetadata:
    """File metadata."""

    path: str
    type: FileType
    size: int
    lines: int
    encoding: str = "utf-8"
    settings: JsonDict = field(default_factory=dict)


@dataclass
class FileContent:
    """File content."""

    content: str
    metadata: FileMetadata
    annotations: dict[str, Any] = field(default_factory=dict)


@dataclass
class FileChange:
    """File change."""

    path: str
    type: ChangeType
    old_path: str | None = None
    diff: str | None = None
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class CodebaseSnapshot:
    """Codebase snapshot."""

    files: Sequence[FileContent]
    timestamp: float
    version: str
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class CodebaseChange:
    """Codebase change."""

    changes: list[FileChange]
    timestamp: float
    version: str
    metadata: JsonDict = field(default_factory=dict)
