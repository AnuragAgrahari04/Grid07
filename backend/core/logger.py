"""Rich-based logger with semantic helper methods used across the project."""

from datetime import datetime

from rich.console import Console
from rich.traceback import install

install(show_locals=False)


class RichLogger:
    def __init__(self) -> None:
        self.console = Console()

    def _log(self, level: str, message: str, style: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S")
        self.console.print(f"[{style}][{ts}] {level:<7}[/{style}] {message}")

    def info(self, message: str) -> None:
        self._log("INFO", message, "cyan")

    def success(self, message: str) -> None:
        self._log("SUCCESS", message, "green")

    def warning(self, message: str) -> None:
        self._log("WARN", message, "yellow")

    def error(self, message: str) -> None:
        self._log("ERROR", message, "red")


log = RichLogger()
