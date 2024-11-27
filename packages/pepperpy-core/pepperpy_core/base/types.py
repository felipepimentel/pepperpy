"""Base type definitions"""

from typing import Any, Dict, TypeAlias, Union

# Basic type aliases
JsonDict: TypeAlias = Dict[str, Any]
JsonValue: TypeAlias = Union[str, int, float, bool, list, dict, None]

# Module specific types
ModuleId: TypeAlias = str
ResourceId: TypeAlias = str

# Configuration types
ConfigKey: TypeAlias = str
ConfigValue: TypeAlias = JsonValue

# Task types
TaskId: TypeAlias = str
TaskResult: TypeAlias = Any

__all__ = [
    "JsonDict",
    "JsonValue",
    "ModuleId",
    "ResourceId",
    "ConfigKey",
    "ConfigValue",
    "TaskId",
    "TaskResult",
]
