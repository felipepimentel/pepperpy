"""Basic console example"""

import asyncio

from pepperpy_console.base import Console


async def main() -> None:
    """Run basic console example"""
    console = Console()

    # Basic output
    console.print("Hello, World!")

    # Styled output
    console.print("[bold blue]Welcome[/] to [green]PepperPy Console[/]!")

    # Different message types
    console.info("This is an info message")
    console.success("This is a success message")
    console.warning("This is a warning message")
    console.error("This is an error message")


if __name__ == "__main__":
    asyncio.run(main())
