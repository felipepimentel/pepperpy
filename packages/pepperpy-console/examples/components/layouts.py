"""Layout examples"""

import asyncio

from pepperpy_console import Console, Layout, Panel, PanelConfig, Table


async def main() -> None:
    """Run layout examples"""
    console = Console()

    # Create components
    table = Table()
    table.add_column("ID")
    table.add_column("Name")
    table.add_column("Status")

    table.add_row("1", "Task 1", "Complete")
    table.add_row("2", "Task 2", "Pending")

    # Create layout
    layout = Layout()
    await layout.split(
        Panel(table, PanelConfig(title="Tasks")),
        Panel("Details will appear here", PanelConfig(title="Details")),
        direction="horizontal",
        ratios=[0.7, 0.3],
    )

    try:
        console.info("Layout example started. Displaying for 5 seconds...")
        # Render layout
        await layout.render()
        await asyncio.sleep(5)  # Keep window open
        console.info("Layout example completed.")
    except Exception as e:
        console.error(f"Error in layout example: {e}")
    finally:
        await layout.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
