from typing import Protocol, Optional, Any, Dict
from dataclasses import dataclass
from ..console import Console

@dataclass
class PluginMetadata:
    """Metadados do plugin."""
    name: str
    version: str
    description: str
    author: Optional[str] = None
    dependencies: Optional[list[str]] = None
    config_schema: Optional[Dict[str, Any]] = None

class Plugin(Protocol):
    """Protocolo base para plugins."""
    
    @property
    def metadata(self) -> PluginMetadata:
        """Retorna metadados do plugin."""
        ...
    
    def initialize(self, app: Any) -> None:
        """Inicializa o plugin."""
        ...
    
    def cleanup(self) -> None:
        """Limpa recursos do plugin."""
        ...
    
    def validate_config(self, config: Dict[str, Any]) -> None:
        """Valida configuração do plugin."""
        ...

class PluginManager:
    """Gerenciador de plugins aprimorado."""
    
    def __init__(self):
        self._plugins: Dict[str, Plugin] = {}
        self._app = None
        self._console: Optional[Console] = None
    
    def register(self, plugin_class: type[Plugin]) -> None:
        """Registra um novo plugin."""
        plugin = plugin_class()
        name = plugin.metadata.name
        
        if name in self._plugins:
            raise ValueError(f"Plugin '{name}' já está registrado")
        
        # Verifica dependências
        if deps := plugin.metadata.dependencies:
            missing = [d for d in deps if d not in self._plugins]
            if missing:
                raise ValueError(
                    f"Plugin '{name}' requer plugins não instalados: {missing}"
                )
        
        self._plugins[name] = plugin
        
        # Inicializa se app já estiver disponível
        if self._app:
            self._initialize_plugin(plugin)
    
    def initialize_all(self, app: Any) -> None:
        """Inicializa todos os plugins."""
        self._app = app
        self._console = app.console
        
        for plugin in self._plugins.values():
            self._initialize_plugin(plugin)
    
    def _initialize_plugin(self, plugin: Plugin) -> None:
        """Inicializa um plugin específico."""
        try:
            # Valida configuração
            if schema := plugin.metadata.config_schema:
                plugin.validate_config(self._app.config)
            
            # Inicializa
            plugin.initialize(self._app)
            
            if self._console:
                self._console.success(
                    f"Plugin '{plugin.metadata.name}' initialized successfully"
                )
                
        except Exception as e:
            if self._console:
                self._console.error(
                    f"Failed to initialize plugin '{plugin.metadata.name}': {e}"
                )
            raise 