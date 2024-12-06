"""DuckDB engine implementation."""

from collections.abc import Callable
from typing import Any, cast

# Define module-level variables
_have_duckdb = False
_duckdb: Any = None
_connect: Callable[..., Any] | None = None

try:
    import duckdb  # type: ignore
    from duckdb import connect  # type: ignore

    _duckdb = duckdb
    _connect = cast(Callable[..., Any], connect)
    _have_duckdb = True
except ImportError:
    pass
