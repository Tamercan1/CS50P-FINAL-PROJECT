from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.live import Live
from rich.markdown import Markdown
import time

console = Console()

def prompt_user(prompt):
    fprompt = Prompt.ask(f"[bold green]{prompt}[/bold green]")
    print()
    return fprompt


def mode_list(modes: dict) -> str:
    table = Table(title="Available Modes")
    table.add_column("Mode", style="magenta", width=20)
    table.add_column("Purpose", style="green", width=40)

    for mode in modes:
        table.add_row(mode, modes[mode])
    print()

    console.print(table)


def print_text(text, title, border_color):
    console.print(Panel(text, title=title, border_style=border_color, width=120, padding=(1, 2)))


def stream_response(resp, mode):
    text = ""

    try:
        with Live(Panel("[dim]Waiting for response...[/dim]", title=mode, border_style="cyan", width=120, padding=(1, 2)), console=console, refresh_per_second=10) as live:

            for chunk in resp:
                piece = getattr(chunk, "text", None)
                if not piece:
                    continue
            
                text += piece
                live.update(
                    Panel(Markdown(text), title=mode, border_style="cyan", width=120, padding=(1, 2))
                )
        
        return text
    except Exception as e:
        console.print("[red]Streaming error occurred.[/red]")
        return text if text else None