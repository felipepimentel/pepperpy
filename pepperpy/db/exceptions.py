"""Database exceptions"""


class DatabaseError(Exception):
    """Base database exception"""

    def __init__(self, message: str, cause: Exception | None = None):
        super().__init__(message)
        self.cause = cause


class ConnectionError(DatabaseError):
    """Database connection error"""

    pass


class QueryError(DatabaseError):
    """Query execution error"""

    pass


class TransactionError(DatabaseError):
    """Transaction error"""

    pass


class ConfigurationError(DatabaseError):
    """Configuration error"""

    pass


class EngineError(DatabaseError):
    """Engine-related error"""

    pass
