from typing import Any, Dict
import os
from dotenv import load_dotenv
from .interfaces import ConfigInterface

class Config(ConfigInterface):
    """Implementação padrão de configurações."""
    
    def __init__(self):
        load_dotenv()
        self._config: Dict[str, Any] = {}
    
    def get(self, key: str, default: Any = None) -> Any:
        """Recupera valor de configuração do ambiente ou dicionário interno."""
        return os.getenv(key) or self._config.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Define um valor de configuração."""
        self._config[key] = value 