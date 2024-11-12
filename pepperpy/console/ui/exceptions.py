"""UI specific exceptions"""

from pepperpy.core.exceptions import CoreError


class UIError(CoreError):
    """Base exception for UI errors"""

    pass


class RenderError(UIError):
    """Error during component rendering"""

    pass


class LayoutError(UIError):
    """Error in layout management"""

    pass


class InputError(UIError):
    """Error handling user input"""

    pass


class ComponentError(UIError):
    """Error in component operation"""

    pass


class ValidationError(UIError):
    """Error in component validation"""

    pass
