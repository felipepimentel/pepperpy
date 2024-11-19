"""AI-related exceptions"""

from pepperpy.core.exceptions import PepperPyError


class AIError(PepperPyError):
    """Base AI error"""


class ClientError(AIError):
    """AI client error"""


class ConfigError(AIError):
    """AI configuration error"""
