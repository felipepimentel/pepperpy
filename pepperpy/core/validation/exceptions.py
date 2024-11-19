"""Validation exceptions"""

from pepperpy.core.exceptions import PepperPyError


class ValidationError(PepperPyError):
    """Base validation error"""


class TypeValidationError(ValidationError):
    """Type validation error"""


class ValueValidationError(ValidationError):
    """Value validation error""" 