"""Extension system for Pepperpy."""
from typing import Dict, Type, Optional
from dataclasses import dataclass
from .interfaces import PepperpyComponent
from .context import ExecutionContext

@dataclass
class ExtensionMetadata:
    """Metadata for Pepperpy extensions."""
    name: str
    version: str
    description: str
    author: str
    dependencies: Dict[str, str]

class Extension(PepperpyComponent):
    """Base class for Pepperpy extensions."""
    
    def __init__(self, context: Optional[ExecutionContext] = None):
        self.context = context or ExecutionContext()
        self._initialized = False
    
    @property
    def metadata(self) -> ExtensionMetadata:
        """Get extension metadata."""
        raise NotImplementedError
    
    @property
    def is_ready(self) -> bool:
        """Check if extension is initialized."""
        return self._initialized
    
    async def initialize(self) -> None:
        """Initialize extension."""
        if not self._initialized:
            await self._do_initialize()
            self._initialized = True
    
    async def _do_initialize(self) -> None:
        """Actual initialization logic."""
        raise NotImplementedError

class ExtensionManager:
    """Manager for Pepperpy extensions."""
    
    def __init__(self, context: Optional[ExecutionContext] = None):
        self.context = context or ExecutionContext()
        self._extensions: Dict[str, Extension] = {}
    
    def register(self, extension_class: Type[Extension]) -> None:
        """Register new extension."""
        extension = extension_class(self.context)
        metadata = extension.metadata
        
        if metadata.name in self._extensions:
            raise ValueError(f"Extension {metadata.name} already registered")
        
        self._extensions[metadata.name] = extension
    
    async def initialize_all(self) -> None:
        """Initialize all registered extensions."""
        for extension in self._extensions.values():
            await extension.initialize()
    
    def get_extension(self, name: str) -> Optional[Extension]:
        """Get extension by name."""
        return self._extensions.get(name) 