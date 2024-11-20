"""Console examples demonstrating UI capabilities"""

import asyncio
from typing import Any

from pepperpy.console import Console
from pepperpy.ui.components import Dialog, Form, Panel, Progress

console = Console()


async def render_and_print(console: Console, content: Any) -> None:
    """Render and print content"""
    try:
        if hasattr(content, "render"):
            rendered = await content.render()
            await console.print(rendered)
        else:
            await console.print(str(content))
    except Exception as e:
        await console.error(f"Failed to render content: {e}")


async def demo_progress() -> None:
    """Demonstrate progress bar"""
    panel = Panel("Progress Demo")
    progress = Progress(
        title="Progress",
        description="Processing",
        current=0,
        total=100,
    )

    try:
        for i in range(0, 101, 5):
            progress.set_progress(i, f"Processing ({i}%)")
            await console.clear()
            await render_and_print(console, panel)
            await render_and_print(console, progress)
            await asyncio.sleep(0.2)

    except Exception as e:
        await console.error(f"Progress demo failed: {e}")


async def demo_form() -> None:
    """Demonstrate form"""
    form = Form("Sample Form")

    async def submit() -> None:
        """Handle form submission"""
        await console.success("Form submitted successfully!")

    form.add_button("📤 Submit", submit)
    await form.initialize()
    await render_and_print(console, form)


async def demo_dialog() -> None:
    """Demonstrate dialog"""
    dialog = Dialog(
        title="Update Available",
        message="A new version is available. Would you like to update now?",
    )

    async def on_update() -> None:
        """Handle update action"""
        await console.success("Update started!")

    async def on_cancel() -> None:
        """Handle cancel action"""
        await console.warning("Update postponed")

    dialog.add_button("🔄 Update Now", on_update, style="green")
    dialog.add_button("⏳ Remind Later", on_cancel, style="yellow")

    await render_and_print(console, dialog)


async def main() -> None:
    """Run console examples"""
    try:
        await demo_progress()
        await demo_form()
        await demo_dialog()

    except KeyboardInterrupt:
        await console.info("Examples finished! 👋")


if __name__ == "__main__":
    asyncio.run(main())
