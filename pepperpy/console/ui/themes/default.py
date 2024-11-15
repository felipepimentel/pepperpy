"""Default theme configuration"""


from rich.style import Style

DEFAULT_THEME: dict[str, Style] = {
    "info": Style(color="cyan"),
    "warning": Style(color="yellow"),
    "error": Style(color="red", bold=True),
    "success": Style(color="green"),
    "highlight": Style(color="cyan", bold=True),
}
