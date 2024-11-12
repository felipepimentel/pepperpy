"""Configuration for console applications"""


class ConsoleConfig:
    def __init__(self, theme: str = "default", refresh_rate: int = 1, force_terminal: bool = False):
        self.theme = theme
        self.refresh_rate = refresh_rate
        self.force_terminal = force_terminal
