# pypepper/__init__.py
from typing import Optional, Dict, Any, Type
from pathlib import Path
import importlib
from .core.application import Application
from .core.config import Config
from .core.plugin import Plugin, PluginManager
from .core.context import ResourceManager
from .core.decorators import cached, retry
from .console import Console, CLI
from .cache import Cache
from .events import EventBus

class Pepperpy:
    """Interface principal do Pepperpy."""
    
    def __init__(
        self,
        config: Optional[Dict[str, Any]] = None,
        plugins: Optional[list[Type[Plugin]]] = None,
        auto_setup: bool = True
    ):
        # Core components
        self._config = Config(config or {})
        self._plugins = PluginManager()
        self._events = EventBus()
        self._cache = Cache()
        self._console = Console()
        self._resources = ResourceManager()
        
        # Register built-in plugins
        if plugins:
            for plugin in plugins:
                self._plugins.register(plugin)
        
        if auto_setup:
            self.setup()
    
    def setup(self) -> None:
        """Configura componentes e plugins."""
        # Initialize plugins
        self._plugins.initialize_all(self)
        
        # Setup event handlers
        self._setup_events()
        
        # Load extensions
        self._load_extensions()
    
    def _setup_events(self) -> None:
        """Configura handlers de eventos padrão."""
        @self._events.on("error")
        async def handle_error(error: Exception):
            self._console.error(f"Error: {str(error)}")
        
        @self._events.on("plugin.loaded")
        async def handle_plugin_loaded(plugin: str):
            self._console.info(f"Plugin loaded: {plugin}")
    
    def _load_extensions(self) -> None:
        """Carrega extensões do diretório de extensões."""
        extensions_dir = Path(self._config.get("extensions_dir", "extensions"))
        if not extensions_dir.exists():
            return
            
        for ext_file in extensions_dir.glob("*.py"):
            try:
                module = importlib.import_module(f".{ext_file.stem}", "extensions")
                if setup_func := getattr(module, "setup", None):
                    setup_func(self)
            except Exception as e:
                self._console.error(f"Failed to load extension {ext_file}: {e}")
    
    @classmethod
    def from_file(cls, path: str, **kwargs) -> "Pepperpy":
        """Inicializa a partir de arquivo de configuração."""
        from .core.config import load_config
        config = load_config(path)
        return cls(config=config, **kwargs)
    
    # Properties para acesso aos componentes
    @property
    def console(self) -> Console:
        return self._console
    
    @property
    def events(self) -> EventBus:
        return self._events
    
    @property
    def cache(self) -> Cache:
        return self._cache
    
    @property
    def plugins(self) -> PluginManager:
        return self._plugins
    
    @property
    def config(self) -> Config:
        return self._config
    
    # Helpers para criação de CLIs
    def create_cli(
        self,
        name: str,
        **kwargs
    ) -> CLI:
        """Cria uma nova CLI com configuração padrão."""
        return CLI(
            name,
            console=self._console,
            plugins=self._plugins,
            **kwargs
        )

