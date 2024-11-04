from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar

from .context import Context
from .events import EventBus
from .health import HealthCheck, HealthMonitor, HealthStatus
from .logging import ContextLogger
from .metadata import ModuleMetadata
from .validation import ModuleValidator, ValidationError

T = TypeVar("T", bound="BaseModule")


@dataclass
class ModuleConfig:
    """Base configuration for all modules"""

    name: str
    enabled: bool = True
    debug: bool = False
    settings: Dict[str, Any] = field(default_factory=dict)


class ModuleBuilder(Generic[T]):
    """Builder pattern for module configuration"""

    def __init__(self, module_class: Type[T]) -> None:
        self._module_class = module_class
        self._config = ModuleConfig(name=module_class.__module_name__)

    def configure(self, **settings) -> "ModuleBuilder[T]":
        """Configure module settings"""
        self._config.settings.update(settings)
        return self

    def enable_debug(self) -> "ModuleBuilder[T]":
        """Enable debug mode"""
        self._config.debug = True
        return self

    def disable(self) -> "ModuleBuilder[T]":
        """Disable module"""
        self._config.enabled = False
        return self

    def build(self) -> T:
        """Build module instance"""
        return self._module_class(self._config)


class BaseModule(ABC):
    """Base class for all PepperPy modules"""

    __module_name__: str
    __version__: str = "0.1.0"
    __description__: str = ""
    __metadata__: Optional[ModuleMetadata] = None
    __validator__: Optional[ModuleValidator] = None
    __dependencies__: list[str] = []

    def __init__(self, config: ModuleConfig) -> None:
        self.config = config
        self._initialized = False
        self._event_bus: Optional[EventBus] = None
        self._context: Optional[Context] = None
        self._health_monitor: Optional[HealthMonitor] = None
        self.logger = ContextLogger(self.__module_name__)

    def _set_event_bus(self, event_bus: EventBus) -> None:
        """Set event bus instance"""
        self._event_bus = event_bus

    def _set_context(self, context: Context) -> None:
        """Set context instance"""
        self._context = context

    def _set_health_monitor(self, monitor: HealthMonitor) -> None:
        """Set health monitor instance"""
        self._health_monitor = monitor

    async def pre_initialize(self) -> None:
        """Hook called before initialization"""
        pass

    async def post_initialize(self) -> None:
        """Hook called after initialization"""
        pass

    async def pre_shutdown(self) -> None:
        """Hook called before shutdown"""
        pass

    async def post_shutdown(self) -> None:
        """Hook called after shutdown"""
        pass

    @classmethod
    def create(cls: Type[T]) -> ModuleBuilder[T]:
        """Create a new module builder"""
        return ModuleBuilder(cls)

    @classmethod
    def get_metadata(cls) -> ModuleMetadata:
        """Get module metadata"""
        if not cls.__metadata__:
            cls.__metadata__ = ModuleMetadata(
                name=cls.__module_name__,
                version=cls.__version__,
                description=cls.__description__,
                dependencies=cls.__dependencies__,
            )
        return cls.__metadata__

    def validate_config(self) -> List[ValidationError]:
        """Validate module configuration"""
        if not self.__validator__:
            return []
        return self.__validator__.validate(self.config.settings)

    async def initialize(self) -> None:
        """Initialize module with validation"""
        errors = self.validate_config()
        if errors:
            raise ValidationError(f"Invalid configuration: {errors}")

        await self.pre_initialize()
        self._initialized = True
        await self.post_initialize()

    @abstractmethod
    async def shutdown(self) -> None:
        """Cleanup module resources"""
        await self.pre_shutdown()
        self._initialized = False
        await self.post_shutdown()

    def configure(self, settings: Dict[str, Any]) -> None:
        """Update module configuration"""
        self.config.settings.update(settings)

    def get_service(self, key: str, service_type: Type[T]) -> T:
        """Get a service from the context"""
        if not self._context:
            raise RuntimeError("Context not initialized")
        return self._context.get(key, service_type)

    def update_health(
        self,
        status: HealthStatus,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Update module health status"""
        if self._health_monitor:
            check = HealthCheck(status, message, details=details)
            self._health_monitor.update(self.__module_name__, check)

    async def check_health(self) -> HealthCheck:
        """Perform module health check"""
        try:
            # Default implementation
            if not self._initialized:
                return HealthCheck(HealthStatus.UNHEALTHY, "Module not initialized")
            return HealthCheck(HealthStatus.HEALTHY, "Module operational")
        except Exception as e:
            return HealthCheck(HealthStatus.UNHEALTHY, f"Health check failed: {str(e)}")
