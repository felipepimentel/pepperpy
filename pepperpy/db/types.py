"""Database types"""

from typing import Any, Dict, Sequence, TypeVar

# Tipo genérico para chaves de dicionário
K = TypeVar("K", str, Any)


class QueryResult:
    """Database query result"""

    def __init__(
        self,
        rows: Sequence[Dict[K, Any]],
        affected_rows: int,
        execution_time: float,
        last_insert_id: Any = None,
    ):
        self.rows = list(rows)  # Convertendo para list para garantir consistência
        self.affected_rows = affected_rows
        self.execution_time = execution_time
        self.last_insert_id = last_insert_id