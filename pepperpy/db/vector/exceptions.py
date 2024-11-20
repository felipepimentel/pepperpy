"""Vector database exceptions"""

from ..exceptions import DatabaseError


class VectorError(DatabaseError):
    """Base exception for vector operations"""


class VectorConfigError(VectorError):
    """Vector configuration error"""


class VectorIndexError(VectorError):
    """Vector index operation error"""


class VectorDimensionError(VectorError):
    """Vector dimension mismatch error""" 