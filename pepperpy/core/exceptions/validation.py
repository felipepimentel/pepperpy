"""Validation-related exceptions"""

from .base import PepperPyError


class ValidationError(PepperPyError):
    """Base validation error"""


class TypeValidationError(ValidationError):
    """Type validation error"""


class ValueValidationError(ValidationError):
    """Value validation error""" 