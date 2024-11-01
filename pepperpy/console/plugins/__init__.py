from typing import Protocol, Dict, Any, Optional, Type
from dataclasses import dataclass
from ..core import Console
from ..cli import CLI

@dataclass
class PluginMetadata:
    """Metadados do plugin."""
    name: str
    version: str
    description: str
    author: Optional[str] = None
    dependencies: Optional[list[str]] = None

class ConsolePlugin(Protocol):
    """Protocolo base para plugins de console."""
    
    @property
    def metadata(self) -> PluginMetadata:
        """Retorna metadados do plugin."""
        ...
    
    def initialize(self, console: Console, cli: Optional[CLI] = None) -> None:
        """Inicializa o plugin."""
        ...
    
    def cleanup(self) -> None:
        """Limpa recursos do plugin."""
        ...

class PluginManager:
    """Gerenciador de plugins para console."""
    
    def __init__(self):
        self._plugins: Dict[str, ConsolePlugin] = {}
        self._console: Optional[Console] = None
        self._cli: Optional[CLI] = None
    
    def register(self, plugin_class: Type[ConsolePlugin]) -> None:
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
        
        # Inicializa se console já estiver disponível
        if self._console:
            plugin.initialize(self._console, self._cli)
    
    def initialize(self, console: Console, cli: Optional[CLI] = None) -> None:
        """Inicializa todos os plugins registrados."""
        self._console = console
        self._cli = cli
        
        for plugin in self._plugins.values():
            plugin.initialize(console, cli)
    
    def cleanup(self) -> None:
        """Limpa recursos de todos os plugins."""
        for plugin in self._plugins.values():
            plugin.cleanup()
            
    def get(self, name: str) -> ConsolePlugin:
        """Obtém plugin por nome."""
        if name not in self._plugins:
            raise KeyError(f"Plugin '{name}' não encontrado")
        return self._plugins[name] 