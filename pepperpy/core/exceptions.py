class PepperError(Exception):
    """Base exception for all PepperPy errors"""

    pass


class ModuleError(PepperError):
    """Base exception for module-related errors"""

    pass


class ModuleNotFoundError(ModuleError):
    """Raised when a module is not found"""

    pass


class DependencyError(ModuleError):
    """Raised when module dependencies are invalid"""

    pass


class ModuleInitializationError(ModuleError):
    """Raised when module initialization fails"""

    pass


class ApplicationError(PepperError):
    """Base exception for application-related errors"""

    pass


class ApplicationStartupError(ApplicationError):
    """Raised when application startup fails"""

    pass
