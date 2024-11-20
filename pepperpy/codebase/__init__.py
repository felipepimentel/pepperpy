"""Code analysis and indexing module for source code management"""

from .config import CodebaseConfig
from .engine import CodebaseEngine
from .indexer import CodeIndexer
from .providers import get_provider
from .types import (
    CodeEntity,
    CodeLocation,
    EntityType,
    IndexEntry,
    RefactorSuggestion,
    ReviewComment,
    ScanResult,
)

__all__ = [
    "CodebaseConfig",
    "CodebaseEngine",
    "CodeIndexer",
    "get_provider",
    # Types
    "CodeEntity",
    "CodeLocation",
    "EntityType",
    "IndexEntry",
    "RefactorSuggestion",
    "ReviewComment",
    "ScanResult",
] 