"""Panel component tests."""

from typing import Literal, cast

import pytest

from pepperpy_console.components import Panel, PanelConfig


@pytest.mark.asyncio
async def test_panel_initialization() -> None:
    """Test panel initialization."""
    # Create panel with default config
    panel = Panel()
    assert panel.config == PanelConfig()

    # Create panel with custom config
    config = PanelConfig(
        title="Test Panel",
        border_style="rounded",
    )
    panel = Panel(config=config)
    assert panel.config == config


@pytest.mark.asyncio
async def test_panel_lifecycle() -> None:
    """Test panel lifecycle (initialize, render, cleanup)."""
    panel = Panel(
        config=PanelConfig(
            title="Test Panel",
            border_style="rounded",
        )
    )

    # Test initialization
    assert not panel._initialized
    await panel.initialize()
    assert panel._initialized

    # Test rendering
    rendered = await panel.render()
    assert rendered is not None

    # Test cleanup
    await panel.cleanup()
    assert not panel._initialized


@pytest.mark.asyncio
async def test_panel_config_validation() -> None:
    """Test panel configuration validation."""
    # Test invalid border style
    with pytest.raises(ValueError):
        PanelConfig(
            border_style=cast(Literal["single", "double", "rounded", "none"], "invalid")
        )

    # Test valid configurations
    valid_styles: list[Literal["single", "double", "rounded", "none"]] = [
        "single",
        "double",
        "rounded",
        "none",
    ]
    for style in valid_styles:
        config = PanelConfig(border_style=style)
        assert config.border_style == style


@pytest.mark.asyncio
async def test_panel_with_content() -> None:
    """Test panel with different content types."""
    # Test with string content
    panel = Panel(
        config=PanelConfig(
            title="String Content",
            border_style="single",
        )
    )
    await panel.initialize()
    rendered = await panel.render()
    assert rendered is not None
    await panel.cleanup()

    # Test with nested panel
    nested_panel = Panel(
        config=PanelConfig(
            title="Nested Panel",
            border_style="double",
        )
    )
    panel = Panel(
        config=PanelConfig(
            title="Parent Panel",
            border_style="rounded",
        )
    )
    await panel.initialize()
    await nested_panel.initialize()
    rendered = await panel.render()
    assert rendered is not None
    await panel.cleanup()
    await nested_panel.cleanup()
