"""Core base classes and interfaces for PepperPy modules"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum, auto
from typing import Any, Dict, List, Optional, Protocol, Type, TypeVar

from .exceptions import ModuleError
from .metrics import Metric, MetricType
from .types import JsonDict

T = TypeVar("T")


class ModuleStatus(Enum):
    """Module lifecycle status"""

    INACTIVE = auto()
    INITIALIZING = auto()
    ACTIVE = auto()
    ERROR = auto()
    SHUTTING_DOWN = auto()


@dataclass
class ModuleConfig:
    """Enhanced base configuration for all modules"""

    enabled: bool = True
    debug: bool = False
    name: Optional[str] = None
    version: str = "1.0.0"
    strict_mode: bool = True
    auto_initialize: bool = True
    timeout: float = 30.0
    retry_attempts: int = 3
    retry_delay: float = 1.0
    metrics_enabled: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)


class ModuleProtocol(Protocol):
    """Protocol defining module interface"""

    async def initialize(self) -> None: ...
    async def cleanup(self) -> None: ...
    def get_status(self) -> ModuleStatus: ...
    def get_metadata(self) -> JsonDict: ...


class BaseModule:
    """Enhanced base class for all PepperPy modules"""

    __module_name__: str = ""
    __dependencies__: List[str] = []
    __optional_dependencies__: List[str] = []
    __version__: str = "1.0.0"

    def __init__(self, config: Optional[ModuleConfig] = None) -> None:
        self.config = config or ModuleConfig(name=self.__module_name__)
        self._status = ModuleStatus.INACTIVE
        self._start_time = datetime.now()
        self._logger = logging.getLogger(f"pepperpy.{self.__module_name__}")
        self._initialized = False
        self._lock = asyncio.Lock()
        self._metrics = None
        self._error: Optional[Exception] = None

    async def initialize(self) -> None:
        """Initialize module with error handling and metrics"""
        if self._initialized:
            return

        try:
            async with self._lock:
                self._status = ModuleStatus.INITIALIZING
                await self._initialize_dependencies()
                await self._initialize_impl()
                self._status = ModuleStatus.ACTIVE
                self._initialized = True
                await self._record_metric("module_initialized")

        except Exception as e:
            self._error = e
            self._status = ModuleStatus.ERROR
            self._logger.error(f"Failed to initialize module: {e}")
            raise ModuleError(f"Module initialization failed: {e}") from e

    async def cleanup(self) -> None:
        """Cleanup module resources with error handling"""
        if not self._initialized:
            return

        try:
            async with self._lock:
                self._status = ModuleStatus.SHUTTING_DOWN
                await self._cleanup_impl()
                self._status = ModuleStatus.INACTIVE
                self._initialized = False
                await self._record_metric("module_cleaned_up")

        except Exception as e:
            self._error = e
            self._status = ModuleStatus.ERROR
            self._logger.error(f"Failed to cleanup module: {e}")
            raise ModuleError(f"Module cleanup failed: {e}") from e

    async def _initialize_impl(self) -> None:
        """Implementation specific initialization"""
        pass

    async def _cleanup_impl(self) -> None:
        """Implementation specific cleanup"""
        pass

    async def _initialize_dependencies(self) -> None:
        """Initialize module dependencies"""
        for dep in self.__dependencies__:
            module = self.get_module(dep)
            if not module:
                raise ModuleError(f"Required dependency not found: {dep}")
            await module.initialize()

    async def _record_metric(self, name: str) -> None:
        """Record module metric"""
        if self._metrics and self.config.metrics_enabled:
            metric = Metric(
                name=f"module_{name}",
                value=1,
                type=MetricType.COUNTER,
                labels={
                    "module": self.__module_name__,
                    "version": self.__version__,
                    "status": self._status.name,
                },
            )
            await self._metrics.record(metric)

    def get_status(self) -> ModuleStatus:
        """Get current module status"""
        return self._status

    def get_metadata(self) -> JsonDict:
        """Get module metadata"""
        return {
            "name": self.__module_name__,
            "version": self.__version__,
            "status": self._status.name,
            "uptime": (datetime.now() - self._start_time).total_seconds(),
            "error": str(self._error) if self._error else None,
            "dependencies": self.__dependencies__,
            "optional_dependencies": self.__optional_dependencies__,
            "config": {k: v for k, v in self.config.__dict__.items() if not k.startswith("_")},
        }

    @classmethod
    def create(cls: Type[T], **kwargs) -> T:
        """Factory method for creating module instances"""
        config = ModuleConfig(**kwargs)
        return cls(config)
