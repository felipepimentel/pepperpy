"""CLI specific exceptions"""

from pepperpy.core.exceptions import CoreError


class CLIError(CoreError):
    """Base exception for CLI errors"""

    pass


class CommandError(CLIError):
    """Error during command execution"""

    pass


class ArgumentError(CLIError):
    """Error in command arguments"""

    pass


class ValidationError(CLIError):
    """Error in argument validation"""

    pass
