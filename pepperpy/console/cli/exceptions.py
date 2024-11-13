"""CLI exceptions"""

from pepperpy.core.exceptions import PepperPyError


class CLIError(PepperPyError):
    """Base CLI error"""


class CommandError(CLIError):
    """Command error"""


class ArgumentError(CLIError):
    """Argument error"""


class ValidationError(CLIError):
    """Validation error"""
