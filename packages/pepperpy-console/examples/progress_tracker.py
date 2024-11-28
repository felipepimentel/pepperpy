"""Example of a progress tracker using pepperpy-console"""

import asyncio
import random
from typing import AsyncGenerator

from pepperpy_console.base import Console
from pepperpy_console.components import Layout, Panel, ProgressBar, Table
from pepperpy_console.components.panel import PanelConfig


class DownloadSimulator:
    """Simulates a download process"""

    async def run(self) -> AsyncGenerator[float, None]:
        """Run download simulation"""
        progress = 0.0
        while progress < 100:
            progress += random.uniform(1, 5)
            progress = min(progress, 100)
            yield progress
            await asyncio.sleep(0.1)


async def main() -> None:
    """Run progress tracker example"""
    console = Console()
    progress_bar = ProgressBar(100)

    # Create table for task details
    table = Table()
    table.add_column("Task")
    table.add_column("Status")
    table.add_column("Progress")

    # Create layout with panels
    layout = Layout()
    await layout.split(
        Panel(progress_bar, PanelConfig(title="Download Progress")),
        Panel(table, PanelConfig(title="Task Details")),
        direction="vertical",
        ratios=[0.3, 0.7],
    )

    # Create and run download simulation
    download = DownloadSimulator()
    try:
        async for progress in download.run():
            progress_bar.set_progress(int(progress))
            table.add_row(
                "Download", "In Progress" if progress < 100 else "Complete", f"{progress:.1f}%"
            )
            await layout.render()

    except Exception as e:
        console.error(f"Task failed: {e}")
    finally:
        if "progress" in locals() and progress >= 100:
            console.success("Download complete!")
        await layout.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
