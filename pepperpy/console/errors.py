from typing import Optional

from pepperpy.core.exceptions import PepperError


class ConsoleError(PepperError):
    """Base exception for console module"""

    pass


class RenderError(ConsoleError):
    """Error rendering console output"""

    def __init__(self, message: str, component: Optional[str] = None):
        self.component = component
        super().__init__(f"Error rendering {component or 'component'}: {message}")


class ValidationError(ConsoleError):
    """Error validating input"""

    def __init__(self, message: str, field: Optional[str] = None):
        self.field = field
        super().__init__(
            f"Validation error{f' for {field}' if field else ''}: {message}"
        )


class InteractionError(ConsoleError):
    """Error during user interaction"""

    pass
