"""File handling exceptions."""


class FileError(Exception):
    """Base exception for file operations."""

    def __init__(self, message: str, *args: object) -> None:
        """Initialize exception.

        Args:
            message: Error message
            *args: Additional arguments
        """
        super().__init__(message, *args)
