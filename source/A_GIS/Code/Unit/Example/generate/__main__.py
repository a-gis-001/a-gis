import sys
import A_GIS.Code.Unit.Example.generate

# Get user input
name = input("Enter the name of the A_GIS functional unit: ").strip()
request = input("Enter a specific request (or press Enter for default): ").strip() or None
background = input("Enter background information (or press Enter to skip): ").strip() or None
model = input("Enter the AI model to use (default: qwen2.5:14b): ").strip() or "qwen2.5:14b"

# Call the generate function
result = A_GIS.Code.Unit.Example.generate(name=name, request=request, background=background, model=model)

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.text import Text

def print_result(result):
    """Prints the output of the generate function in a conversational and structured format."""
    console = Console()

    console.print(Panel("[bold cyan]A_GIS Report Generation[/bold cyan]", title="🔍 Summary"))

    console.print(f"[bold]Functional Unit Name:[/bold] {result._name}", style="bold magenta")
    console.print(f"[bold]Request:[/bold] {result._request}", style="bold magenta")
    console.print(f"[bold]Background:[/bold] {result._background if result._background else 'None'}", style="bold magenta")
    console.print(f"[bold]Model Used:[/bold] {result._model}", style="bold magenta")

    console.print("\n[bold cyan]Processing Summary:[/bold cyan]")
    if result.error:
        console.print(Panel(f"[red]Error:[/red] {result.error}", title="❌ Error"))
    else:
        console.print("\n[bold]Prompt Sent to AI:[/bold]", style="yellow")
        console.print(Markdown(result.prompt))

        console.print("\n[bold]System Message:[/bold]", style="yellow")
        console.print(Markdown(result.system))

        console.print("\n[bold green]Generated Conversation:[/bold green]")

        # Check if result.result contains messages
        if hasattr(result.result, "messages") and isinstance(result.result.messages, list):
            for message in result.result.messages:
                role = message.get("role", "unknown").capitalize()
                content = message.get("content", "").strip()

                if role == "System":
                    console.print(Panel(Markdown(content), title="🖥️ System", border_style="yellow"))
                elif role == "User":
                    console.print(Panel(Markdown(content), title="🧑‍💻 User", border_style="blue"))
                elif role == "Assistant":
                    console.print(Panel(Markdown(content), title="🤖 Assistant", border_style="green"))
                else:
                    console.print(Panel(Markdown(content), title=f"💬 {role}", border_style="gray"))
        else:
            console.print("[gray]No conversation found.[/gray]")

    console.print("\n[bold cyan]End of Report[/bold cyan]")

print_result(result)
