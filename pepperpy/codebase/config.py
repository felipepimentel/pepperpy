"""Codebase configuration"""

from dataclasses import dataclass, field
from enum import Enum

from pepperpy.core.types import JsonDict


class ProviderType(str, Enum):
    """Supported code analysis providers"""

    STATIC = "static"
    HYBRID = "hybrid"


@dataclass
class CodebaseConfig:
    """Configuration for code analysis"""

    provider: ProviderType = ProviderType.STATIC
    max_file_size: int = 1024 * 1024  # 1MB
    ignore_patterns: list[str] = field(
        default_factory=lambda: ["*.pyc", "__pycache__", "*.egg-info", "dist", "build"]
    )
    parse_docstrings: bool = True
    track_dependencies: bool = True
    analyze_complexity: bool = True
    metadata: JsonDict = field(default_factory=dict)
