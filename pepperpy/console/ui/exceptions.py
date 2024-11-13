"""Console UI exceptions"""

from pepperpy.core.exceptions import PepperPyError


class UIError(PepperPyError):
    """Base UI error"""


class RenderError(UIError):
    """Render error"""


class InputError(UIError):
    """Input error"""


class LayoutError(UIError):
    """Layout error"""
