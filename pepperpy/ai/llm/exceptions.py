"""LLM exceptions"""

from pepperpy.core.exceptions import PepperPyError


class LLMError(PepperPyError):
    """Base exception for LLM errors"""


class ProviderError(LLMError):
    """Error during provider operations"""


class ConfigurationError(LLMError):
    """Error in LLM configuration"""


class GenerationError(LLMError):
    """Error during text generation"""
