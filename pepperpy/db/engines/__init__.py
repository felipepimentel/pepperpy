"""Database engines"""

from typing import Any, Dict

from ..config import DatabaseConfig
from .base import BaseEngine
from .postgres import PostgresEngine
from .sqlite import SQLiteEngine


def get_engine(config: Dict[str, Any]) -> BaseEngine:
    """Get database engine based on configuration"""
    engine_type = config.get("engine", "sqlite")

    # Convert dictionary config to DatabaseConfig object
    db_config = DatabaseConfig(**config)

    if engine_type == "postgres":
        return PostgresEngine(db_config)
    elif engine_type == "sqlite":
        return SQLiteEngine(db_config)
    else:
        raise ValueError(f"Unsupported database engine: {engine_type}")
