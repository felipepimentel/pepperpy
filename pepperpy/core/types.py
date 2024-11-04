from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Optional, TypeVar, Union

# Type variables
T = TypeVar("T")
R = TypeVar("R")

# Common type aliases
JsonDict = Dict[str, Any]
PathLike = Union[str, Path]
OptionalStr = Optional[str]
CallbackType = Callable[..., Any]


# Common base classes
@dataclass
class BaseConfig:
    """Base configuration class"""

    enabled: bool = True
    debug: bool = False
    settings: JsonDict = field(default_factory=dict)


@dataclass
class Metadata:
    """Base metadata class"""

    name: str
    version: str
    description: OptionalStr = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
