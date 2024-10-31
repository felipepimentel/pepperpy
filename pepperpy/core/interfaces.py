from abc import ABC, abstractmethod
from typing import Optional

class LLMInterface(ABC):
    """Interface base para Large Language Models."""
    
    @abstractmethod
    def chat(self, 
            messages: list[dict[str, str]], 
            model: Optional[str] = None,
            temperature: float = 0.7,
            max_tokens: Optional[int] = None) -> dict:
        """
        Envia mensagens para o LLM e retorna a resposta.
        
        Args:
            messages: Lista de mensagens no formato [{role: str, content: str}]
            model: Nome do modelo (opcional)
            temperature: Temperatura para geração (0.0 a 1.0)
            max_tokens: Limite máximo de tokens na resposta
            
        Returns:
            dict: Resposta do modelo com campos 'content' e 'usage'
        """
        pass
    
    @abstractmethod
    def complete(self, 
                prompt: str,
                model: Optional[str] = None,
                temperature: float = 0.7,
                max_tokens: Optional[int] = None) -> dict:
        """
        Envia um prompt único para completar.
        
        Args:
            prompt: Texto do prompt
            model: Nome do modelo (opcional)
            temperature: Temperatura para geração (0.0 a 1.0)
            max_tokens: Limite máximo de tokens na resposta
            
        Returns:
            dict: Resposta do modelo com campos 'content' e 'usage'
        """
        pass 