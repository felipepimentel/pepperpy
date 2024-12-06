"""Progress tracker example."""

import asyncio
import random

from pepperpy_console import (
    Layout,
    LayoutConfig,
    Panel,
    PanelConfig,
    ProgressBar,
    ProgressConfig,
)


async def simulate_task(progress: ProgressBar) -> None:
    """Simulate a task with progress updates.

    Args:
        progress: Progress bar to update
    """
    total_steps = progress.config.total
    for step in range(total_steps + 1):
        progress.update(step)
        await asyncio.sleep(random.uniform(0.1, 0.3))


async def main() -> None:
    """Run progress tracker example."""
    # Create layout
    main_layout = Layout(
        config=LayoutConfig(
            direction="vertical",
            spacing=1,
        )
    )

    # Create progress bars
    task1_progress = ProgressBar(
        config=ProgressConfig(
            total=50,
            description="Task 1",
            style="blue",
        )
    )

    task2_progress = ProgressBar(
        config=ProgressConfig(
            total=30,
            description="Task 2",
            style="green",
        )
    )

    # Create panels
    task1_panel = Panel(
        config=PanelConfig(
            title="Task 1 Progress",
            border_style="rounded",
        )
    )

    task2_panel = Panel(
        config=PanelConfig(
            title="Task 2 Progress",
            border_style="rounded",
        )
    )

    # Initialize components
    await main_layout.initialize()
    await task1_progress.initialize()
    await task2_progress.initialize()

    # Split layout
    await main_layout.split(task1_panel, task2_panel)

    # Start tasks
    task1 = asyncio.create_task(simulate_task(task1_progress))
    task2 = asyncio.create_task(simulate_task(task2_progress))

    # Update display while tasks run
    try:
        while not (task1.done() and task2.done()):
            await main_layout.render()
            await asyncio.sleep(0.1)
    finally:
        # Cleanup
        await main_layout.cleanup()
        await task1_progress.cleanup()
        await task2_progress.cleanup()


if __name__ == "__main__":
    asyncio.run(main())
