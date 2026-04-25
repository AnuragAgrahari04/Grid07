from rich.console import Console
from rich.pretty import Pretty

from personas.bots import BOT_PERSONAS
from phase2.engine import run_content_engine

console = Console()


def run() -> None:
    console.rule("[bold cyan]Phase 2 Test - LangGraph Content Engine")
    for bot in BOT_PERSONAS:
        console.print(f"\n[bold]Running for {bot.bot_id} ({bot.name})[/bold]")
        output = run_content_engine(bot.bot_id)
        console.print(Pretty(output))


if __name__ == "__main__":
    run()
