from rich.console import Console
from rich.table import Table

from phase1.router import route_post_to_bots

console = Console()

TEST_POSTS = [
    "OpenAI just released a new model that might replace junior developers.",
    "Fed raises rates again. Yield curve inversion deepens.",
    "Big Tech companies are harvesting your data and selling it to governments.",
]


def run() -> None:
    console.rule("[bold cyan]Phase 1 Test - Vector Persona Router")
    for idx, post in enumerate(TEST_POSTS, start=1):
        result = route_post_to_bots(post)
        console.print(f"\n[bold]Test {idx}[/bold]")
        console.print(f"Post: {post}")

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Bot")
        table.add_column("Similarity", justify="right")
        table.add_column("Will Respond", justify="center")

        for score in result.all_scores:
            table.add_row(
                score.bot_name,
                f"{score.similarity_score:.4f}",
                "YES" if score.will_respond else "NO",
            )

        console.print(table)


if __name__ == "__main__":
    run()
