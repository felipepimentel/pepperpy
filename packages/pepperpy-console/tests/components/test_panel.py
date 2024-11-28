"""Test panel component"""

from io import StringIO

import pytest
from pepperpy_console.components import Panel, Table
from pepperpy_console.components.panel import PanelConfig
from rich.console import Console as RichConsole
from rich.panel import Panel as RichPanel


@pytest.fixture
def panel() -> Panel:
    """Create test panel"""
    return Panel("Test Content", PanelConfig(title="Test Panel", style="blue"))


@pytest.mark.asyncio
async def test_panel_initialization(panel: Panel) -> None:
    """Test panel initialization"""
    assert panel.content == "Test Content"
    assert panel.config.title == "Test Panel"
    assert panel.config.style == "blue"


@pytest.mark.asyncio
async def test_panel_render(panel: Panel) -> None:
    """Test panel rendering"""
    console = RichConsole(file=StringIO(), force_terminal=True)
    rendered = await panel.render()
    console.print(rendered)
    output = console.file.getvalue()  # type: ignore
    assert "Test Content" in output
    assert "Test Panel" in output


@pytest.mark.asyncio
async def test_panel_with_component() -> None:
    """Test panel with nested component"""
    console = RichConsole(file=StringIO(), force_terminal=True)
    table = Table()
    table.add_column("Test")
    table.add_row("Value")

    panel = Panel(table, PanelConfig(title="Table Panel"))
    rendered = await panel.render()
    console.print(rendered)
    output = console.file.getvalue()  # type: ignore
    assert "Table Panel" in output
    assert "Value" in output


@pytest.fixture
def rich_console() -> RichConsole:
    """Create Rich console for testing"""
    return RichConsole(file=StringIO(), force_terminal=True, color_system="truecolor", width=80)


@pytest.mark.asyncio
async def test_panel_styling(panel: Panel, rich_console: RichConsole) -> None:
    """Test panel styling"""
    rendered = await panel.render()

    # Verify panel was rendered correctly
    assert isinstance(rendered, RichPanel)

    # Check panel style
    style = rendered.style
    assert style is not None

    # Style can be either a string or RichStyle object
    if isinstance(style, str):
        assert style == "blue"
    else:
        assert hasattr(style, "color")
        assert style.color.name == "blue"  # type: ignore

    # Verify rendered output with ANSI codes
    rich_console.print(rendered)
    output = rich_console.file.getvalue()  # type: ignore
    assert "\x1b[34m" in output  # ANSI code for blue
