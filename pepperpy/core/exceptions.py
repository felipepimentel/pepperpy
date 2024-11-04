"""Core exceptions for PepperPy."""


class PepperError(Exception):
    """Base exception for all PepperPy errors."""

    pass


class ConfigurationError(PepperError):
    """Raised when there is a configuration error."""

    pass


class ValidationError(PepperError):
    """Raised when validation fails."""

    pass


class ModuleInitializationError(PepperError):
    """Raised when a module fails to initialize."""

    pass


class ModuleNotFoundError(PepperError):
    """Raised when a required module is not found."""

    pass


class ServiceNotFoundError(PepperError):
    """Raised when a required service is not found in the context."""

    pass


class ApplicationStartupError(PepperError):
    """Raised when the application fails to start."""

    pass


class DependencyError(PepperError):
    """Raised when there is a dependency error."""

    pass


class ContextError(PepperError):
    """Raised when there is a context error."""

    pass
