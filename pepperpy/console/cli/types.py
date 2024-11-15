"""CLI type definitions"""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from pepperpy.core.types import JsonDict


@dataclass
class Command:
    """Command definition"""

    name: str
    callback: Callable
    help: str
    arguments: list[str] = field(default_factory=list)
    options: list[str] = field(default_factory=list)
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class Option:
    """Command option definition"""

    name: str
    type_: type = str
    default: Any = None
    help: str = ""
    required: bool = False
    multiple: bool = False
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class Argument:
    """Command argument definition"""

    name: str
    type_: type = str
    help: str = ""
    required: bool = True
    metadata: JsonDict = field(default_factory=dict)
