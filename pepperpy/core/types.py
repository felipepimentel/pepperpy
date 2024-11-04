from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, Generic, List, Optional, TypeVar, Union

# Type aliases
JsonDict = Dict[str, Any]
PathLike = Union[str, Path]

# Generic type for modules
T = TypeVar("T")


class Status(str, Enum):
    """Status padrão para operações"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    ERROR = "error"
    WARNING = "warning"


@dataclass
class ModuleConfig:
    """Configuração base para módulos"""

    name: str
    enabled: bool = True
    debug: bool = False
    settings: JsonDict = field(default_factory=dict)
    dependencies: List[str] = field(default_factory=list)

    @classmethod
    def create(cls) -> "ModuleConfig":
        """Factory method para criar configuração"""
        return cls(name="")


@dataclass
class Metadata:
    """Metadados para módulos e componentes"""

    name: str
    version: str
    description: Optional[str] = None
    author: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Result(Generic[T]):
    """Resultado padronizado para operações"""

    success: bool
    data: Optional[T] = None
    error_message: Optional[str] = None
    metadata: JsonDict = field(default_factory=dict)

    @classmethod
    def ok(cls, data: T, **metadata) -> "Result[T]":
        """Cria resultado de sucesso"""
        return cls(success=True, data=data, metadata=metadata)

    @classmethod
    def fail(cls, message: str, **metadata) -> "Result[T]":
        """Cria resultado de erro"""
        return cls(success=False, error_message=message, metadata=metadata)
