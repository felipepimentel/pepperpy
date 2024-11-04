from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional, Type, TypeVar

from .config import ConfigurationProvider
from .context import Context
from .events import EventBus
from .exceptions import (
    ApplicationStartupError,
    DependencyError,
    ModuleInitializationError,
    ValidationError,
)
from .health import HealthCheck, HealthMonitor
from .logging import ContextLogger
from .metadata import MetadataProvider, ModuleMetadata
from .module import BaseModule

T = TypeVar("T", bound=BaseModule)


class Application:
    """Main application container"""

    def __init__(self, config_provider: Optional[ConfigurationProvider] = None) -> None:
        self._modules: Dict[str, BaseModule] = {}
        self._event_bus = EventBus()
        self._context = Context()
        self._config_provider = config_provider
        self._metadata = MetadataProvider()
        self._initialized = False
        self._health_monitor = HealthMonitor()
        self.logger = ContextLogger("application")

    def register_service(self, key: str, instance: Any) -> "Application":
        """Register a service in the context"""
        self._context.register(key, instance)
        return self

    def add_module(self, module: BaseModule) -> "Application":
        """Add a module with all required components"""
        module._set_event_bus(self._event_bus)
        module._set_context(self._context)
        module._set_health_monitor(self._health_monitor)

        with self.logger.context(module=module.__module_name__):
            self.logger.info("Registering module")

            # Register metadata
            self._metadata.register(module.get_metadata())

            # Apply and validate configuration
            if self._config_provider:
                config = self._config_provider.get_config(module.__module_name__)
                module.configure(config)
                errors = module.validate_config()
                if errors:
                    self.logger.error("Invalid configuration", extra={"errors": errors})
                    raise ValidationError(
                        f"Invalid configuration for module '{module.__module_name__}': {errors}"
                    )

            self._modules[module.config.name] = module
            self.logger.info("Module registered successfully")

        return self

    def get_module(self, name: str, expected_type: Type[T]) -> T:
        """Get a module by name and type"""
        module = self._modules.get(name)
        if not module:
            raise ModuleNotFoundError(f"Module '{name}' not found")
        if not isinstance(module, expected_type):
            raise TypeError(f"Module '{name}' is not of type {expected_type.__name__}")
        return module

    def list_modules(self, tag: Optional[str] = None) -> List[ModuleMetadata]:
        """List registered modules"""
        return self._metadata.list_modules(tag)

    @asynccontextmanager
    async def run(self):
        """Run the application"""
        await self._start()
        try:
            yield self
        finally:
            await self._shutdown()

    async def _start(self) -> None:
        """Start all modules"""
        if self._initialized:
            return

        try:
            self._validate_dependencies()

            # Initialize modules in order
            for module in self._get_initialization_order():
                if module.config.enabled:
                    try:
                        await module.initialize()
                    except Exception as e:
                        raise ModuleInitializationError(
                            f"Failed to initialize module '{module.config.name}': {str(e)}"
                        ) from e

            self._initialized = True

        except Exception as e:
            # Cleanup any initialized modules on error
            await self._shutdown()
            raise ApplicationStartupError("Failed to start application") from e

    async def _shutdown(self) -> None:
        """Shutdown all modules"""
        if not self._initialized:
            return

        # Shutdown in reverse order
        for module in reversed(self._get_initialization_order()):
            if module._initialized:
                await module.shutdown()

        self._initialized = False

    def _validate_dependencies(self) -> None:
        """Validate module dependencies"""
        for name, module in self._modules.items():
            for dep in module.__dependencies__:
                if dep not in self._modules:
                    raise DependencyError(
                        f"Module '{name}' depends on '{dep}' which is not registered"
                    )

    def _get_initialization_order(self) -> list[BaseModule]:
        """Get modules in dependency order"""
        visited = set()
        order = []

        def visit(name: str) -> None:
            if name in visited:
                return
            module = self._modules[name]
            for dep in module.__dependencies__:
                visit(dep)
            visited.add(name)
            order.append(module)

        for name in self._modules:
            visit(name)

        return order

    async def check_health(self) -> Dict[str, HealthCheck]:
        """Check health of all modules"""
        for module in self._modules.values():
            if module.config.enabled:
                check = await module.check_health()
                self._health_monitor.update(module.config.name, check)
        return self._health_monitor.get_all()
