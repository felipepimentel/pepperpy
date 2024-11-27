"""File handling exceptions"""


class FileError(Exception):
    """Base exception for file operations"""

    def __init__(self, message: str, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause
