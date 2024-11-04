"""Core exceptions for PepperPy."""

from typing import Any, Dict, Optional


class PepperError(Exception):
    """Exceção base para todos os erros"""

    def __init__(
        self,
        message: str,
        code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.code = code or self.__class__.__name__
        self.details = details or {}
        super().__init__(message)


class ConfigError(PepperError):
    """Erro de configuração"""

    pass


class ValidationError(PepperError):
    """Erro de validação"""

    def __init__(self, message: str, field: Optional[str] = None):
        super().__init__(
            message,
            code="VALIDATION_ERROR",
            details={"field": field} if field else None,
        )


class ModuleError(PepperError):
    """Erro relacionado a módulos"""

    def __init__(self, message: str, module_name: str):
        super().__init__(message, code="MODULE_ERROR", details={"module": module_name})


class DependencyError(ModuleError):
    """Erro de dependência entre módulos"""

    pass


class StateError(PepperError):
    """Erro de estado da aplicação"""

    pass


class ResourceError(PepperError):
    """Erro relacionado a recursos"""

    pass


class OperationError(PepperError):
    """Erro em operações"""

    pass
