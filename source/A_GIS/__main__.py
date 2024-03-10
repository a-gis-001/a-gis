import rich_click as click
import A_GIS.Cli.register
import A_GIS.Cli.get_console_width
import rich.traceback

rich.traceback.install()

# Width for terminals.
WIDTH = A_GIS.Cli.get_console_width(max_width=120)


# Define a group to hold subcommands
@click.rich_config(
    help_config=click.RichHelpConfiguration(use_markdown=True, width=WIDTH)
)
@click.group()
def cli():
    pass


# Define the inspect command.
@click.command()
@A_GIS.Cli.register
def inspect(
    module_name: "module to inspect",
    *,
    methods: "show methods" = True,
    more: "show more including full docstring" = False,
):
    """Inspect an A_GIS module"""
    import importlib
    import rich

    module = importlib.import_module(module_name)
    console = rich.console.Console(width=WIDTH)
    rich.inspect(module, console=console, methods=methods, help=more)


cli.add_command(inspect)


# Define the update command.
@click.command()
@A_GIS.Cli.register
def update(*, root: "path to find A_GIS root" = "source/A_GIS"):
    """Update the A_GIS repo tree"""
    import A_GIS.Code.Tree.update
    import A_GIS.Code.Tree.recurse
    import A_GIS.Code.find_root
    import subprocess
    import pathlib
    import rich

    # Perform the update.
    console = rich.console.Console(width=WIDTH)
    root = A_GIS.Code.find_root(path=pathlib.Path(root))

    console.print(f"updating A_GIS at root={root}...")
    tree = A_GIS.Code.Tree.recurse(path=root)
    A_GIS.Code.Tree.update(tree=tree)

    command = ["git", "-c", "color.ui=always", "status", f"{root}"]
    completed_process = subprocess.run(
        command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True
    )

    # Get the command output
    command_output = completed_process.stdout
    lines = command_output.splitlines()
    stripped_lines = [line.rstrip() for line in lines]
    command_output = "\n".join(stripped_lines)

    command_output = command_output.replace("\t", "    ")
    # Create a Text object with the command output for styling
    output_text = rich.text.Text.from_ansi(command_output)
    panel = rich.panel.Panel(
        output_text, title=f"git status {root}", expand=True, border_style="bold cyan"
    )

    # Use the console to render the output inside a box, capturing the result
    console.print(panel)


cli.add_command(update)


# Define the name command.
@click.command()
@A_GIS.Cli.register
def name(path: "path to code to determine name"):
    import A_GIS.Code.Unit.Name.init_from_path
    import pathlib

    path = pathlib.Path(path).resolve()
    name = A_GIS.Code.Unit.Name.init_from_path(path=path)
    console = rich.console.Console(width=WIDTH)
    console.print(name)


cli.add_command(name)

# This is always a main.
cli()
