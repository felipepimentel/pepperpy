"""Transform types."""

from dataclasses import dataclass, field
from typing import Any

JsonDict = dict[str, Any]


@dataclass
class FormatOptions:
    """Code formatting options."""

    line_length: int = 88
    indent_size: int = 4
    quote_style: str = "double"
    trailing_comma: bool = True
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class RefactorOptions:
    """Code refactoring options."""

    max_line_length: int = 88
    max_complexity: int = 10
    max_function_length: int = 50
    extract_threshold: int = 3
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class TransformResult:
    """Transform result."""

    original: str
    transformed: str
    changes: list[str]
    metadata: JsonDict = field(default_factory=dict)
