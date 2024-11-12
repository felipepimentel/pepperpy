"""Plugin system exceptions"""

from pepperpy.core.exceptions import CoreError


class PluginError(CoreError):
    """Base exception for plugin errors"""

    pass


class PluginLoadError(PluginError):
    """Error loading plugin"""

    pass


class PluginNotFoundError(PluginError):
    """Plugin not found"""

    pass


class PluginValidationError(PluginError):
    """Plugin validation error"""

    pass
