# pypepper/__init__.py
__version__ = "0.1.0"


def lazy_import(module_name):
    """Helper function to lazily import a module."""
    import importlib

    return importlib.import_module(module_name)


# Essential imports (example: logging, often used)
from .logging import get_logger
