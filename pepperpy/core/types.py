"""Core type definitions and custom types"""

import json
from datetime import date, datetime
from pathlib import Path
from typing import Any, Dict, Protocol, TypeVar, Union

# Type aliases
PathLike = Union[str, Path]
JsonDict = Dict[str, Any]
Timestamp = Union[datetime, date, str, float]

# Generic types
T = TypeVar("T")
K = TypeVar("K")
V = TypeVar("V")


class Serializable(Protocol):
    """Protocol for serializable objects"""

    def to_dict(self) -> JsonDict: ...

    @classmethod
    def from_dict(cls, data: JsonDict) -> "Serializable": ...


class JsonEncoder(json.JSONEncoder):
    """Enhanced JSON encoder with support for additional types"""

    def default(self, obj: Any) -> Any:
        if isinstance(obj, (datetime, date)):
            return obj.isoformat()
        if isinstance(obj, Path):
            return str(obj)
        if isinstance(obj, Serializable):
            return obj.to_dict()
        return super().default(obj)


# Common type validators
def is_path_like(value: Any) -> bool:
    """Check if value is path-like"""
    return isinstance(value, (str, Path))


def is_json_serializable(value: Any) -> bool:
    """Check if value is JSON serializable"""
    try:
        json.dumps(value, cls=JsonEncoder)
        return True
    except (TypeError, ValueError):
        return False
