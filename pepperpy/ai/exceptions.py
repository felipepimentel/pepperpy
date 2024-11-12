"""AI module exceptions"""

from pepperpy.core.exceptions import CoreError


class AIError(CoreError):
    """Base exception for AI errors"""

    pass


class ModelError(AIError):
    """Model-related error"""

    pass


class ProviderError(AIError):
    """Provider-related error"""

    pass


class ValidationError(AIError):
    """Validation error"""

    pass
