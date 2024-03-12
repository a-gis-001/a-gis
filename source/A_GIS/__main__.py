import rich_click as click
import A_GIS.Cli.register
import A_GIS.Cli.get_console_width
import rich.traceback
import rich

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
    import A_GIS.Cli.get_git_status

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
    import A_GIS.Code.Unit.move
    import A_GIS.Cli.update_and_show_git_status

    console = rich.console.Console(width=WIDTH)
    console.print(f"Moving old={old} to new={new}")
    old_path, new_path = A_GIS.Code.Unit.move(old=old, new=new)
    console.print(f"Finished with old_path={old_path} to new_path={new_path}")

    # Update all the files, doing formatting and performing checks.
    root = A_GIS.Code.find_root(path=old_path)
    panel = A_GIS.Cli.update_and_show_git_status(root=root)
    console.print(panel)


cli.add_command(move)


# Define the catalog command.
@click.command()
@A_GIS.Cli.register
def catalog(args: bool = True):
    """Show a catalog of all of A_GIS"""
    import A_GIS.catalog
    import A_GIS.Code.highlight

    console = rich.console.Console(width=WIDTH)
    index = 0
    for code in A_GIS.catalog(include_args=args):
        index += 1
        output_text = rich.text.Text.from_ansi(A_GIS.Code.highlight(code=code))
        name, _ = code.split("(", 1)
        rule = rich.rule.Rule(align="left", style="bright white", title=str(index))
        console.print(rule)
        console.print(code, "\n")


cli.add_command(catalog)


# Define the docstring command.
@click.command()
@A_GIS.Cli.register
def docstring(name: "unit name"):
    """Use AI to replace a docstring"""
    import A_GIS.Code.Unit.Name.init_from_path
    import A_GIS.Code.Unit.Name.to_path
    import A_GIS.File.read
    import A_GIS.Code.find_root
    import A_GIS.Code.Docstring.generate
    import A_GIS.Code.Docstring.modify
    import pathlib
    import A_GIS.File.write
    import A_GIS.Cli.get_git_status
    import A_GIS.Cli.update_and_show_git_status

    # Get the path and name.
    if "." in name:
        path = A_GIS.Code.Unit.Name.to_path(name=name) / "__init__.py"
    else:
        path = pathlib.Path(name)
        name = A_GIS.Code.Unit.Name.init_from_path(path=path)
        if path.is_dir():
            path /= "__init__.py"
    console = rich.console.Console(width=WIDTH)
    console.print(f"Replacing docstring for unit name={name} at path={path} ...")

    # Generate a docstring.
    code = A_GIS.File.read(file=path)
    docstring = A_GIS.Code.Docstring.generate(name=name, code=code)
    panel = rich.panel.Panel(
        docstring, title=f"new docstring", expand=True, border_style="bold cyan"
    )
    console.print(panel)

    # Write the new docstring into the file.
    console.print(f"Writing new docstring to {path} ...")
    code = A_GIS.Code.Docstring.modify(code=code, docstring=docstring)
    A_GIS.File.write(content=code, file=path)

    # Update all the files, doing formatting and performing checks.
    root = A_GIS.Code.find_root(path=path)
    panel = A_GIS.Cli.update_and_show_git_status(root=root)
    console.print(panel)


cli.add_command(docstring)


# Define the touch command.
@click.command()
@A_GIS.Cli.register
def touch(name: "unit name"):
    """Create a new unit"""
    import A_GIS.Code.Unit.touch
    import os
    import subprocess

    # Touch the file.
    console = rich.console.Console(width=WIDTH)
    console.print(f"Touching name={name}")
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
    import A_GIS.Code.Unit.Name.generate

    # Try three times.
    console = rich.console.Console(width=WIDTH)
    console.print(
        f"Initiating AI name generation with description='{description}' tries={tries}"
    )
    names = []
    for i in range(tries):
        name = A_GIS.Code.Unit.Name.generate(description=description, temperature=0.9)
        console.print(f"AI generated name={name}")
        if len(name) > len("A_GIS."):
            names.append(name)
        else:
            console.print(f"Discarding name={name} for improper format")

    console.print(f"Entering final name selection with suggestions={names}")
    name = A_GIS.Code.Unit.Name.generate(
        description=description, suggestions=names, temperature=0.5
    )
    console.print(f"name={name}")


cli.add_command(name)


# Define the logserver command.
@click.command()
@A_GIS.Cli.register
def logserver(port: "port to use" = 9999):
    import socket
    import os

    host, port = os.environ.get("A_GIS_LOGSERVER", "localhost:9999").split(":")
    port = int(port)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        console = rich.console.Console(width=WIDTH)
        console.print(f"Log server listening on host {host} port {port} ...")
        server_socket.bind((host, port))
        server_socket.listen()

        conn, addr = server_socket.accept()
        with conn:
            console.print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                # Decode and print the log message
                console.print(data.decode("utf-8"))


cli.add_command(logserver)

# This is always a main.
cli()
