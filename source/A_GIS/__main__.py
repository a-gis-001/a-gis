import A_GIS.catalog
import A_GIS.Cli.get_console_width
import A_GIS.Cli.get_git_status
import A_GIS.Cli.get_name_and_path
import A_GIS.Cli.register
import A_GIS.Cli.update_and_show_git_status
import A_GIS.Code.Docstring.generate
import A_GIS.Code.replace_docstring
import A_GIS.Code.Docstring.fix_short_description
import A_GIS.Code.find_root
import A_GIS.Code.highlight
import A_GIS.Code.Tree.recurse
import A_GIS.Code.Tree.update
import A_GIS.Code.Unit.move
import A_GIS.Code.Unit.Name.generate
import A_GIS.Code.Unit.Name.init_from_path
import A_GIS.Code.Unit.Name.to_path
import A_GIS.Code.Unit.touch
import A_GIS.File.read
import A_GIS.File.write
import importlib
import io
import os
import pathlib
import rich
import rich_click as click
import rich.traceback
import socket
import subprocess
import sys

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

    module = importlib.import_module(module_name)
    console = rich.console.Console(width=WIDTH)
    rich.inspect(module, console=console, methods=methods, help=more)


cli.add_command(inspect)


# Define the update command.
@click.command()
@A_GIS.Cli.register
def update(*, root: "path to find A_GIS root" = "source/A_GIS"):
    """Update the A_GIS repo tree"""

    # Perform the update.
    console = rich.console.Console(width=WIDTH)
    root = A_GIS.Code.find_root(path=pathlib.Path(root))

    console.print(f"updating A_GIS at root={root} ...")
    tree = A_GIS.Code.Tree.recurse(path=root)
    A_GIS.Code.Tree.update(tree=tree)

    # Use the console to render the output inside a box, capturing the result
    console.print(A_GIS.Cli.get_git_status(root=root))


cli.add_command(update)


# Define the move command.
@click.command()
@A_GIS.Cli.register
def move(old: "old unit name", new: "new unit name"):
    """Move an A_GIS functional unit from one name/location to another"""

    console = rich.console.Console(width=WIDTH)
    console.print(f"Moving old={old} to new={new}")
    old_path, new_path = A_GIS.Code.Unit.move(old=old, new=new)
    console.print(f"Finished with old_path={old_path} to new_path={new_path}")

    # Update all the files, doing formatting and performing checks.
    root = A_GIS.Code.find_root(path=new_path)
    panel = A_GIS.Cli.update_and_show_git_status(root=root)
    console.print(panel)


cli.add_command(move)


# Define the catalog command.
@click.command()
@A_GIS.Cli.register
def catalog(args: bool = True):
    """Show a catalog of all of A_GIS"""

    # Use StringIO to capture the rich output into a buffer
    output_buffer = io.StringIO()

    # Use a Console that writes to the buffer
    console = rich.console.Console(file=output_buffer, width=WIDTH, force_terminal=True)

    index = 0
    for code in A_GIS.catalog(include_args=args):
        index += 1
        output_text = rich.text.Text.from_ansi(A_GIS.Code.highlight(code=code))
        rule = rich.rule.Rule(align="left", style="bright white", title=str(index))
        console.print(rule)
        console.print(code, "\n")

    # Retrieve the buffer content
    output_content = output_buffer.getvalue()

    # Use click to page the output
    click.echo_via_pager(output_content)


cli.add_command(catalog)


# Define the list command.
@click.command()
@A_GIS.Cli.register
@click.option("--color", type=bool, default=None, help="Force color output (default: auto-detect)")
def list(tests: bool = False, mains: bool = False, local: bool = False, color: bool = None):
    """Show a list of all of A_GIS"""
    import A_GIS.Code.list

    # Auto-detect color support: enabled for TTY, disabled for redirected output
    if color is None:
        color = sys.stdout.isatty()

    ignore=[]
    if not tests:
        ignore.append('tests')
    if not mains:
        ignore.append('__main__')
    if not local:
        ignore.append('_')

    console = rich.console.Console(width=WIDTH, force_terminal=color)
    for f in A_GIS.Code.list(ignore=ignore).result:
        parts = f.split('.')  # Split by dots for qualified names
        colored_text = rich.console.Text()

        for i,part in enumerate(parts):
            if part.islower():
                colored_text.append(part, style="green")
            elif part.startswith("_"):
                colored_text.append(part, style="orange")
            else:
                colored_text.append(part)

            if i < len(parts) - 1:
                colored_text.append(".", style="white")

        console.print(colored_text)

cli.add_command(list)


# Define the docstring command.
@click.command()
@A_GIS.Cli.register
def docstring(name: "unit name (ALL for all staged)", *, root: "path to A_GIS root" = "source/A_GIS", model: "model name" = "wizardlm2:7b"):
    """Use AI to replace a docstring"""

    # Get the path and name.
    if name=="ALL":
        status = A_GIS.Code.Unit.get_git_status(root=root)
        names = [name for name in status.staged_names if not name == 'A_GIS']
    else:
        names = [name]

    for name in names:
        name, path = A_GIS.Cli.get_name_and_path(arg=name)
        console = rich.console.Console(width=WIDTH)
        console.print(f"Replacing docstring for [bold]{name}[/bold] at path={path} ...")

        # Generate a docstring.
        code = A_GIS.File.read(file=path)
        docstring = A_GIS.Code.Docstring.generate(name=name, code=code, model=model, reformat=True)
        panel = rich.panel.Panel(
            str(docstring), title=f"new docstring", expand=True, border_style="bold cyan"
        )
        console.print(panel)

        # Write the new docstring into the file.
        console.print(f"Writing new docstring to path={path} ...")
        code = A_GIS.Code.replace_docstring(code=code, docstring=docstring)
        A_GIS.File.write(content=code, file=path)

    # Update all the files, doing formatting and performing checks.
    root = A_GIS.Code.find_root(path=root)
    panel = A_GIS.Cli.update_and_show_git_status(root=root)
    console.print(panel)


cli.add_command(docstring)


# Define the touch command.
@click.command()
@A_GIS.Cli.register
def touch(name: "unit name"):
    """Create a new unit"""

    # Touch the file.
    console = rich.console.Console(width=WIDTH)
    console.print(f"Touching [bold]{name}[/bold]")
    path = A_GIS.Code.Unit.touch(name=name)

    # Update all the files, doing formatting and performing checks.
    root = A_GIS.Code.find_root(path=path)
    console.print(f"Updating A_GIS at root={root} ...")
    panel = A_GIS.Cli.update_and_show_git_status(root=root)
    console.print(panel)

    # Open in the editor if environment variable defined.
    if "EDITOR" in os.environ:
        subprocess.run([os.environ.get("EDITOR"), str(path)])
    else:
        console.print("TIP: Define environmental variable EDITOR to open touched file!")


cli.add_command(touch)


# Define the name command.
@click.command()
@A_GIS.Cli.register
def name(description: "unit description", tries: "number of tries" = 3):
    """Generate a new name from a description"""

    console = rich.console.Console(width=WIDTH)
    console.print(
        f"Initiating AI name generation with description='{description}' tries={tries}"
    )

    # Try a few times.
    names = []
    for i in range(tries):
        x = A_GIS.Code.Unit.Name.generate(description=description)
        console.print(f"AI generated name={name}")
        if len(x.names) > 0:
            names = x.names
            break

    if len(names)==0:
        console.print("Could not get AI to give a valid name!")
    else:
        console.print(f"name={name}")

cli.add_command(name)


# Define the add command.
@click.command()
@A_GIS.Cli.register
def add(name: "unit name"):
    """Wrapper around git add"""

    # Get the path and name.
    name, path = A_GIS.Cli.get_name_and_path(arg=name)
    console = rich.console.Console(width=WIDTH)
    path0 = str(path.parent)
    root = A_GIS.Code.find_root(path=path)
    console.print(f"Adding to staged package/unit [bold]{name}[/bold] at path={path0} ...")

    A_GIS.Cli.run_git(mode='add',args=[str(path0)])
    panel = A_GIS.Cli.update_and_show_git_status(root=root)
    console.print(panel)


cli.add_command(add)


# Define the distill command.
@click.command()
@A_GIS.Cli.register
def distill(name: "unit name" = ""):
    """Distill a piece of code into its basic form"""

    if name == "":
        names = A_GIS.Code.list(ignore=["__main", "tests"]).result.keys()
    else:
        names = [name]

    console = rich.console.Console(width=WIDTH)
    A_GIS.Cli.distill(console=console, names=names)


cli.add_command(distill)


# Define the commit command.
@click.command()
@A_GIS.Cli.register
def commit(*, root: "path to A_GIS root" = "source/A_GIS", dry_run: "just generate message without committing" = False):
    """Use AI to generate a commit message for the staged changes"""

    # Show current status.
    root = A_GIS.Code.find_root(path=root)
    console = rich.console.Console(width=WIDTH)
    console.print(f"Generating commit message for A_GIS at root={root} ...")
    panel = A_GIS.Cli.update_and_show_git_status(root=root)
    console.print(panel)

    # Get the commit message.
    message = A_GIS.Code.CommitMessage.generate(do_commit=not dry_run)
    panel = rich.panel.Panel(
        message, title=f"commit message", expand=True, border_style="bold cyan"
    )
    console.print(panel)

cli.add_command(commit)


# Define the status command.
@click.command()
@A_GIS.Cli.register
def status(*, root: "path to A_GIS root" = "source/A_GIS"):
    """Show git status"""

    # Show current status.
    console = rich.console.Console(width=WIDTH)
    status = A_GIS.Code.Unit.get_git_status(root=root)
    output_text = rich.text.Text.from_ansi("\n".join(status.staged_names))
    panel = rich.panel.Panel(
        output_text,
        title=f"staged",
        expand=True,
        border_style="bold green",
    )
    console.print(panel)
    output_text = rich.text.Text.from_ansi("\n".join(status.modified_names))
    panel = rich.panel.Panel(
        output_text,
        title=f"modified",
        expand=True,
        border_style="bold red",
    )
    console.print(panel)

cli.add_command(status)

# This is always a main.
cli()
