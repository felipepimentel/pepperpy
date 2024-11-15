"""Console CLI application"""

import asyncio

from pepperpy.core.logging import get_logger

from ..ui import ConsoleApp


class CLIApp:
    """CLI application"""

    def __init__(self):
        self._app: ConsoleApp | None = None
        self._logger = get_logger(__name__)

    async def initialize(self) -> None:
        """Initialize application"""
        try:
            self._app = ConsoleApp()
            await self._app.initialize()
            await self._logger.async_.info("CLI application initialized")
        except Exception as e:
            await self._logger.async_.error(f"Failed to initialize CLI application: {e!s}")
            raise

    async def run(self) -> None:
        """Run application"""
        if not self._app:
            await self._logger.async_.error("CLI application not initialized")
            return

        try:
            await self._app.run()
        except Exception as e:
            await self._logger.async_.error(f"CLI application error: {e!s}")
            raise
        finally:
            await self.cleanup()

    async def cleanup(self) -> None:
        """Cleanup application resources"""
        if self._app:
            try:
                await self._app.cleanup()
                await self._logger.async_.info("CLI application cleaned up")
            except Exception as e:
                await self._logger.async_.error(f"Failed to cleanup CLI application: {e!s}")
                raise


def main() -> None:
    """Main entry point"""
    app = CLIApp()
    try:
        asyncio.run(app.run())
    except KeyboardInterrupt:
        asyncio.run(app.cleanup())
