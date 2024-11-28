"""Parser type definitions"""

from dataclasses import dataclass
from typing import Any

from bko.core.types import JsonDict


@dataclass
class ParseResult:
    """Code parsing result"""

    ast: Any
    imports: list[str]
    metadata: JsonDict