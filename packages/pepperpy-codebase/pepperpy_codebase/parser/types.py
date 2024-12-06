"""Parser types."""

from collections.abc import Sequence
from dataclasses import dataclass, field
from typing import Any

JsonDict = dict[str, Any]


@dataclass
class ImportInfo:
    """Import information."""

    name: str
    module: str
    alias: str | None = None
    is_from: bool = False
    level: int = 0
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class FunctionInfo:
    """Function information."""

    name: str
    args: Sequence[str]
    returns: str | None = None
    is_async: bool = False
    is_generator: bool = False
    decorators: list[str] = field(default_factory=list)
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class ClassInfo:
    """Class information."""

    name: str
    bases: Sequence[str]
    methods: Sequence[FunctionInfo]
    is_dataclass: bool = False
    decorators: list[str] = field(default_factory=list)
    metadata: JsonDict = field(default_factory=dict)


@dataclass
class ModuleInfo:
    """Module information."""

    path: str
    imports: Sequence[ImportInfo]
    functions: Sequence[FunctionInfo]
    classes: Sequence[ClassInfo]
    docstring: str | None = None
    metadata: JsonDict = field(default_factory=dict)
