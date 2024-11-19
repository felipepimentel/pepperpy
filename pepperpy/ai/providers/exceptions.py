"""Provider-related exceptions"""

from pepperpy.core.exceptions import PepperPyError


class ProviderError(PepperPyError):
    """Base provider error"""


class ProviderConfigError(ProviderError):
    """Provider configuration error"""


class ProviderConnectionError(ProviderError):
    """Provider connection error"""


class ProviderResponseError(ProviderError):
    """Provider response error""" 