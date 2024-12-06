"""Enums module for file types and operations."""

from enum import Enum


class FileType(str, Enum):
    """File type enum."""

    TEXT = "text"
    BINARY = "binary"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"
    CONFIG = "config"
    ARCHIVE = "archive"
    UNKNOWN = "unknown"


class FileOperation(str, Enum):
    """File operation enum."""

    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    MOVE = "move"
    COPY = "copy"
