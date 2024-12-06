"""Test configuration and fixtures for pepperpy-console.

Note: It's normal to have multiple conftest.py files in different test directories.
Each one provides fixtures specific to its package's tests.
"""

import pytest

from pepperpy_console import (
    ChatConfig,
    ChatView,
    Layout,
    Panel,
    PanelConfig,
    ProgressBar,
    ProgressConfig,
)


@pytest.fixture
def panel() -> Panel:
    """Create test panel"""
    return Panel(config=PanelConfig())


@pytest.fixture
def layout() -> Layout:
    """Create test layout"""
    return Layout()


@pytest.fixture
def progress_bar() -> ProgressBar:
    """Create test progress bar"""
    return ProgressBar(
        config=ProgressConfig(
            total=100,
            description="Test Progress",
        )
    )


@pytest.fixture
def chat_view() -> ChatView:
    """Create test chat view"""
    return ChatView(config=ChatConfig())
