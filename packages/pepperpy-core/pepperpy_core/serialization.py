"""Serialization utilities."""

import json
from dataclasses import asdict, is_dataclass
from typing import Any, TypeVar, cast

T = TypeVar("T")


def serialize(obj: Any) -> bytes:
    """Serialize object to bytes."""
    if is_dataclass(obj):
        data = asdict(cast(Any, obj))
    elif isinstance(obj, dict):
        data = obj
    else:
        data = {"value": obj}

    return json.dumps(data).encode()


def deserialize(data: bytes, cls: type[T] | None = None) -> T | dict[str, Any]:
    """Deserialize bytes to object."""
    result = json.loads(data.decode())
    if cls and is_dataclass(cls):
        return cast(T, cls(**result))
    return cast(dict[str, Any], result)
