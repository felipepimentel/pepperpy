"""Codebase configuration."""

from dataclasses import dataclass, field

from .types import FileType, JsonDict


@dataclass
class IndexConfig:
    """Index configuration."""

    enabled: bool = True
    max_file_size: int = 1024 * 1024  # 1MB
    excluded_paths: list[str] = field(default_factory=list)
    included_types: list[FileType] = field(default_factory=lambda: list(FileType))
    settings: JsonDict = field(default_factory=dict)


@dataclass
class SearchConfig:
    """Search configuration."""

    max_results: int = 100
    max_context_lines: int = 3
    fuzzy_matching: bool = True
    case_sensitive: bool = False
    settings: JsonDict = field(default_factory=dict)


@dataclass
class CodebaseConfig:
    """Codebase configuration."""

    name: str
    root_path: str
    index: IndexConfig = field(default_factory=IndexConfig)
    search: SearchConfig = field(default_factory=SearchConfig)
    metadata: JsonDict = field(default_factory=dict)
