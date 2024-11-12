"""Configuration specific exceptions"""

from pepperpy.core.exceptions import CoreError


class ConfigError(CoreError):
    """Base exception for configuration errors"""

    pass


class ValidationError(ConfigError):
    """Configuration validation error"""

    pass


class LoadError(ConfigError):
    """Configuration loading error"""

    pass


class SaveError(ConfigError):
    """Configuration saving error"""

    pass
