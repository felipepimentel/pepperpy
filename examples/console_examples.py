"""Console examples demonstrating UI capabilities"""

import asyncio

from pepperpy.console import Console
from pepperpy.console.ui.components import Dialog, Form, FormField, ProgressBar

console = Console()


async def demonstrate_basic_console() -> None:
    """Demonstrate basic console functionality"""
    try:
        # Basic printing
        console.print("Hello from PepperPy!")
        console.info("This is an info message")

        # Styled messages
        console.success("Operation completed successfully!")
        console.error("Something went wrong!")
        console.warning("Be careful!")

    except Exception as e:
        console.error("Basic console demo failed", str(e))


async def demonstrate_progress() -> None:
    """Demonstrate progress bar"""
    try:
        progress = ProgressBar(total=100)
        await progress.initialize()

        try:
            console.info("Starting progress demonstration...")
            
            for i in range(0, 101, 10):
                progress.set_progress(i, f"Progress: {i}%")
                await asyncio.sleep(0.5)
                
            console.success("Progress complete!")
        finally:
            await progress.cleanup()

    except Exception as e:
        console.error("Progress demo failed", str(e))


async def demonstrate_dialog() -> None:
    """Demonstrate dialog component"""
    try:
        dialog = Dialog()
        await dialog.initialize()

        try:
            dialog.message = "Do you want to continue?"
            dialog.add_button("Yes", lambda: console.print("Confirmed!"))
            dialog.add_button("No", lambda: console.print("Cancelled!"))
            
            console.print(await dialog.render())
        finally:
            await dialog.cleanup()

    except Exception as e:
        console.error("Dialog demo failed", str(e))


async def demonstrate_form() -> None:
    """Demonstrate form component"""
    try:
        form = Form()
        await form.initialize()

        try:
            # Criar campos do formulário corretamente
            name_field = FormField(name="name", label="Name")
            email_field = FormField(name="email", label="Email")
            
            form.add_field(name_field)
            form.add_field(email_field)
            form.add_button("Submit", lambda: console.print("Form submitted!"))
            
            console.print(await form.render())
        finally:
            await form.cleanup()

    except Exception as e:
        console.error("Form demo failed", str(e))


async def main() -> None:
    """Run console examples"""
    try:
        await demonstrate_basic_console()
        await demonstrate_progress()
        await demonstrate_dialog()
        await demonstrate_form()
    except KeyboardInterrupt:
        console.info("\nExamples finished! 👋")


if __name__ == "__main__":
    asyncio.run(main())
