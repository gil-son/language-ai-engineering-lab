from rich.console import Console
from rich.text import Text

def print_llm_result(prompt, response):
    console = Console()

    console.print(Text("USER PROMPT:", style="bold green"))
    console.print(Text(prompt, style="bold blue"), end="\n\n")

    console.print(Text("LLM RESPONSE:", style="bold green"))
    console.print(Text(response.content, style="bold blue"), end="\n\n")

    usage = response.response_metadata.get("token_usage")

    if usage:
        console.print(f"[bold white]Input tokens:[/bold white] [bright_black]{usage['prompt_tokens']}[/bright_black]")
        console.print(f"[bold white]Output tokens:[/bold white] [bright_black]{usage['completion_tokens']}[/bright_black]")
        console.print(f"[bold white]Total tokens:[/bold white] [bright_black]{usage['total_tokens']}[/bright_black]")
    else:
        console.print("[bold yellow]Token usage not available for this model/provider.[/bold yellow]")

    console.print(f"[yellow]{'-'*50} [/yellow]")