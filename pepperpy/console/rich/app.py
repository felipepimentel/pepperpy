"""Rich console implementation"""


from rich.console import Console as RichConsole
from rich.layout import Layout
from rich.live import Live

from ..core.app import ConsoleApp
from ..core.config import ConsoleConfig


class RichConsoleApp(ConsoleApp):
    """Rich-based console implementation"""

    def __init__(self, config: ConsoleConfig | None = None):
        super().__init__(config or ConsoleConfig())
        self.console = RichConsole()
        self._layout = Layout()
        self._live: Live | None = None

    async def start(self) -> None:
        """Start rich console"""
        self._setup_layout()
        self._live = Live(
            self._layout,
            console=self.console,
            refresh_per_second=1,
        )
        self._live.start()

    async def stop(self) -> None:
        """Stop rich console"""
        if self._live:
            self._live.stop()

    def _setup_layout(self) -> None:
        """Setup default layout"""
        self._layout.split(
            Layout(name="header", size=3),
            Layout(name="main"),
            Layout(name="footer", size=3),
        )


class RichApp:
    pass


__all__ = ["RichApp"]
