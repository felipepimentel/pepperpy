"""Database type definitions"""

from dataclasses import dataclass, field
from typing import Any, Sequence


@dataclass
class QueryResult:
    """Database query result"""

    rows: Sequence[dict[str, Any]]
    affected_rows: int
    execution_time: float
    metadata: dict[str, Any] = field(default_factory=dict)
