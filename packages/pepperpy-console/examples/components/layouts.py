"""Layout example."""

import asyncio

from pepperpy_console import Layout, LayoutConfig, Panel, PanelConfig


async def main() -> None:
    """Run layout example."""
    # Create main layout
    main_layout = Layout(
        config=LayoutConfig(
            direction="vertical",
            spacing=1,
        )
    )

    # Create panels
    header = Panel(
        config=PanelConfig(
            title="Header",
            border_style="rounded",
        )
    )

    content = Panel(
        config=PanelConfig(
            title="Content",
            border_style="double",
        )
    )

    footer = Panel(
        config=PanelConfig(
            title="Footer",
            border_style="single",
        )
    )

    # Initialize layout
    await main_layout.initialize()

    # Split layout into panels
    await main_layout.split(header, content, footer)

    # Render layout
    await main_layout.render()

    # Cleanup
    await main_layout.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
