"""Test configuration and fixtures"""

import pytest
from pepperpy_console import (
    ChatView,
    Console,
    ConsoleConfig,
    Layout,
    ProgressBar,
    Table,
)


@pytest.fixture
def console() -> Console:
    """Create test console"""
    return Console(ConsoleConfig())


@pytest.fixture
def layout() -> Layout:
    """Create test layout"""
    return Layout()


@pytest.fixture
def table() -> Table:
    """Create test table"""
    table = Table()
    table.add_column("Col 1")
    table.add_column("Col 2")
    return table


@pytest.fixture
def progress_bar() -> ProgressBar:
    """Create test progress bar"""
    return ProgressBar(total=100)


@pytest.fixture
def chat_view() -> ChatView:
    """Create test chat view"""
    return ChatView()
