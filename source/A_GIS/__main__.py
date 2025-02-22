import A_GIS
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
@click.command("inspect")
@A_GIS.Cli.register
def cli_inspect(
    module_name: "module to inspect",
    *,
    methods: "show methods" = True,
    more: "show more including full docstring" = False,
):
    """Inspect an A_GIS module"""

    module = importlib.import_module(module_name)
    console = rich.console.Console(width=WIDTH)
    rich.inspect(module, console=console, methods=methods, help=more)


cli.add_command(cli_inspect)


# Define the update command.
@click.command("update")
@A_GIS.Cli.register
def cli_update(*, root: "path to find A_GIS root" = "source/A_GIS"):
    """Update the A_GIS repo tree"""

    # Perform the update.
    console = rich.console.Console(width=WIDTH)
    root = A_GIS.Code.find_root(path=pathlib.Path(root))

    console.print(f"updating A_GIS at root={root} ...")

    # Update the tree
    tree = A_GIS.Code.Tree.recurse(path=root)
    A_GIS.Code.Tree.update(tree=tree)

    # Show git status
    console.print(A_GIS.Cli.get_git_status(root=root))


cli.add_command(cli_update)


# Define the move command.
@click.command("move")
@A_GIS.Cli.register
def cli_move(old: "old unit name", new: "new unit name"):
    """Move an A_GIS functional unit from one name/location to another"""

    console = rich.console.Console(width=WIDTH)
    console.print(f"Moving old={old} to new={new}")
    old_path, new_path = A_GIS.Code.Unit.move(old=old, new=new)
    console.print(f"Finished with old_path={old_path} to new_path={new_path}")

    # Update all the files, doing formatting and performing checks.
    root = A_GIS.Code.find_root(path=new_path)
    panel = A_GIS.Cli.update_and_show_git_status(root=root)
    console.print(panel)


cli.add_command(cli_move)


# Define the catalog command.
@click.command("catalog")
@A_GIS.Cli.register
def cli_catalog(args: bool = True):
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


cli.add_command(cli_catalog)


# Define the list command.
@click.command("list")
@A_GIS.Cli.register
@click.option(
    "--color", type=bool, default=None, help="Force color output (default: auto-detect)"
)
def cli_list(
    tests: bool = False, mains: bool = False, local: bool = False, color: bool = None
):
    """Show a list of all of A_GIS"""
    # Auto-detect color support: enabled for TTY, disabled for redirected output
    if color is None:
        color = sys.stdout.isatty()

    ignore = []
    if not tests:
        ignore.append("tests")
    if not mains:
        ignore.append("__main__")
    if not local:
        ignore.append("_")

    console = rich.console.Console(width=WIDTH, force_terminal=color)
    for f in A_GIS.Code.list(ignore=ignore).result:
        parts = f.split(".")  # Split by dots for qualified names
        colored_text = rich.console.Text()

        for i, part in enumerate(parts):
            if part.islower():
                colored_text.append(part, style="green")
            elif part.startswith("_"):
                colored_text.append(part, style="orange")
            else:
                colored_text.append(part)

            if i < len(parts) - 1:
                colored_text.append(".", style="white")

        console.print(colored_text)


cli.add_command(cli_list)


# Define the docstring command.
@click.command("docstring")
@A_GIS.Cli.register
def cli_docstring(
    name: "unit name (ALL for all staged)",
    *,
    root: "path to A_GIS root" = "source/A_GIS",
    model: "model name" = "wizardlm2:7b",
):
    """Use AI to replace a docstring"""

    # Get the path and name.
    if name == "ALL":
        status = A_GIS.Code.Unit.get_git_status(root=root)
        names = [name for name in status.staged_names if not name == "A_GIS"]
    else:
        names = [name]

    for name in names:
        name, path = A_GIS.Cli.get_name_and_path(arg=name)
        console = rich.console.Console(width=WIDTH)
        console.print(f"Replacing docstring for [bold]{name}[/bold] at path={path} ...")

        # Generate a docstring.
        code = A_GIS.File.read(file=path)
        docstring = A_GIS.Code.Docstring.generate(
            name=name, code=code, model=model, reformat=True
        )
        panel = rich.panel.Panel(
            str(docstring),
            title=f"new docstring",
            expand=True,
            border_style="bold cyan",
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


cli.add_command(cli_docstring)


# Define the touch command.
@click.command("touch")
@A_GIS.Cli.register
def cli_touch(name: "unit name"):
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


cli.add_command(cli_touch)


# Define the absorb command.
@click.command("absorb")
@A_GIS.Cli.register
def cli_absorb(
    file: "function to absorb",
    *,
    name: "name to place" = None,
    write: "whether to write" = True,
):
    """Absorb a function into A_GIS"""

    console = rich.console.Console(width=WIDTH)
    console.print(f"Absorbing function file={file}")
    code = A_GIS.File.read(file=file)
    x = A_GIS.Code.Unit.absorb(code=code, name=name, write=write)

    if x.error:
        console.print(f"Function could not be absorbed\n{x.error}")
    else:
        if x.generated_names:
            console.print("Names generated:")
            for name in x.generated_names:
                console.print(f"  - {name}")
        if write:
            console.print(
                f"New function absorbed to [bold]{x.name}[/bold] at path={str(x.path)}!"
            )
        else:
            console.print(
                f"New function would be absorbed to [bold]{x.name}[/bold] at path={str(x.path)}!"
            )


cli.add_command(cli_absorb)


# Define the add command.
@click.command("add")
@A_GIS.Cli.register
def cli_add(name: "unit name"):
    """Wrapper around git add"""

    # Get the path and name.
    name, path = A_GIS.Cli.get_name_and_path(arg=name)
    console = rich.console.Console(width=WIDTH)
    path0 = str(path.parent)
    root = A_GIS.Code.find_root(path=path)
    console.print(
        f"Adding to staged package/unit [bold]{name}[/bold] at path={path0} ..."
    )

    A_GIS.Cli.run_git(mode="add", args=[str(path0)])
    panel = A_GIS.Cli.update_and_show_git_status(root=root)
    console.print(panel)


cli.add_command(cli_add)


# Define the distill command.
@click.command("distill")
@A_GIS.Cli.register
def cli_distill(name: "unit name" = ""):
    """Distill a piece of code into its basic form"""

    if name == "":
        names = A_GIS.Code.list(ignore=["__main", "tests"]).result.keys()
    else:
        names = [name]

    console = rich.console.Console(width=WIDTH)
    A_GIS.Cli.distill(console=console, names=names)


cli.add_command(cli_distill)


# Define the commit command.
@click.command("commit")
@A_GIS.Cli.register
def cli_commit(
    *,
    root: "path to A_GIS root" = "source/A_GIS",
    dry_run: "just generate message without committing" = False,
):
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


cli.add_command(cli_commit)


# Define the status command.
@click.command("status")
@A_GIS.Cli.register
def cli_status(*, root: "path to A_GIS root" = "source/A_GIS"):
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


cli.add_command(cli_status)

@click.command('repl')
@A_GIS.Cli.register
def cli_repl(ctx=None, debug:"Show debug info"=False):
    """Interactive REPL to explore A_GIS modules"""
    import rich
    from rich.text import Text
    from rich.tree import Tree
    from prompt_toolkit import PromptSession
    from prompt_toolkit.completion import Completer, Completion
    import importlib
    import inspect
    from collections import deque

    console = rich.console.Console(width=WIDTH)
    if debug:
        console.print("Starting REPL...")
        console.print(f"Current sys.argv: {sys.argv}")
        console.print("Initializing navigation...")

    nav_history = deque(maxlen=10)

    class PathCompleter(Completer):
        def __init__(self, get_current_contents):
            self.get_current_contents = get_current_contents

        def get_completions(self, document, complete_event):
            text = document.text_before_cursor

            # Handle root navigation
            if text.endswith('/'):
                try:
                    root_module = A_GIS
                    contents = get_module_contents(root_module)
                    for name in contents.keys():
                        yield Completion(name, start_position=-1)
                except:
                    pass
                return

            # Handle going up
            if text.endswith('../'):
                if path_stack:
                    parent_path = path_stack[-1]
                    try:
                        parent_module = importlib.import_module(parent_path)
                        contents = get_module_contents(parent_module)
                        for name in contents.keys():
                            yield Completion(name, start_position=-2)
                    except:
                        pass
                return

            # Handle module paths
            if '.' in text:
                parts = text.split('.')
                base = '.'.join(parts[:-1])
                partial = parts[-1]

                try:
                    full_path = f"{current_path}.{base}" if base else current_path
                    module = importlib.import_module(full_path)
                    contents = get_module_contents(module)

                    for name in contents.keys():
                        if name.startswith(partial):
                            yield Completion(name, start_position=-len(partial))
                except:
                    pass
                return

            # Default completion from current module
            contents = self.get_current_contents()
            for name in contents.keys():
                if name.startswith(text):
                    yield Completion(name, start_position=-len(text))

            # Add basic commands
            commands = ['..', 'help', 'exit', '/']
            for cmd in commands:
                if cmd.startswith(text):
                    yield Completion(cmd, start_position=-len(text))

    def get_module_contents(module):
        """Get contents of a module"""
        contents = {}
        try:
            for name, obj in inspect.getmembers(module):
                if name.startswith('_'):
                    continue

                # Only include if it's part of A_GIS
                obj_name = getattr(obj, '__name__', '')
                if not isinstance(obj_name, str) or (inspect.ismodule(obj) and not obj_name.startswith('A_GIS')):
                    continue

                if inspect.ismodule(obj):
                    contents[name] = ('module', obj)
                elif inspect.isfunction(obj):
                    contents[name] = ('function', obj)
                elif inspect.isclass(obj):
                    contents[name] = ('class', obj)
        except Exception as e:
            if debug:
                console.print(f"[red]Error getting contents: {str(e)}[/red]")
        return contents

    def show_nav_tree():
        """Display navigation history as a tree"""
        tree = Tree("A_GIS", style="bold", guide_style="bold bright_black")
        current_nodes = {"A_GIS": tree}

        for path, type_, obj in nav_history:
            parts = path.split('.')
            current = "A_GIS"

            # Handle modules first
            for part in parts[1:]:  # Skip "A_GIS" as it's the root
                parent = current
                current = f"{current}.{part}"
                if current not in current_nodes:
                    style = "green" if current == path and type_ == 'module' else "bold white"
                    # Get module description
                    try:
                        module = importlib.import_module(current)
                        doc = inspect.getdoc(module)
                        desc = ""
                        if doc:
                            first_line = doc.split('\n')[0]
                            desc = f" # {first_line}"
                    except:
                        desc = ""
                    label = f"{part}{desc}"
                    current_nodes[current] = current_nodes[parent].add(
                        label,
                        style=style,
                        guide_style="bold bright_black"
                    )

            # Add function or class if this history entry is one
            if type_ in ('function', 'class'):
                style = "cyan" if type_ == 'function' else "magenta"
                name = parts[-1]
                doc = inspect.getdoc(obj)
                desc = ""
                if doc:
                    first_line = doc.split('\n')[0]
                    desc = f" # {first_line}"
                if type_ == 'function':
                    sig = str(inspect.signature(obj))
                    label = f"○ {name}{sig}{desc}"
                    # Force long signatures to single line
                    if len(label) > console.width - 20:  # Leave some margin
                        label = label.replace('\n', ' ')
                    current_nodes[current].add(label, style=style, guide_style="bold bright_black")
                else:
                    current_nodes[current].add(f"□ {name}{desc}", style=style, guide_style="bold bright_black")

        console.print("\nNavigation History:")
        console.print(tree)
        console.print()

    def show_contents(contents):
        """Display current module contents"""
        if not contents:
            console.print("[dim]Empty module[/dim]")
            return

        table = rich.table.Table(show_header=True, show_edge=True, border_style="bold")
        table.add_column("Type", style="dim")
        table.add_column("Name", style="bold")
        table.add_column("Description")

        for name, (type_, obj) in sorted(contents.items()):
            doc = inspect.getdoc(obj)
            desc = doc.split('\n')[0] if doc else "No description"
            style = {"module": "green", "function": "cyan", "class": "magenta"}[type_]
            table.add_row(type_.capitalize(), Text(name, style=style), desc)

        console.print(table)
        console.print()

    try:
        if debug:
            console.print("Initializing navigation...")

        current_path = "A_GIS"
        current_module = A_GIS
        path_stack = []

        contents = get_module_contents(current_module)
        if debug:
            console.print(f"Found {len(contents)} items")

        completer = PathCompleter(lambda: contents)
        session = PromptSession(completer=completer)

        # Banner
        console.print("[bold]A_GIS Explorer[/bold]")
        console.print("Type [cyan]module.submodule[/cyan] + TAB to explore")
        console.print("Type [cyan]../[/cyan] + TAB to see parent contents")
        console.print("Type [cyan]/[/cyan] + TAB to see root contents")
        console.print("Type [green]help[/green] for commands\n")

        # Show initial contents
        show_contents(contents)

        while True:
            try:
                if len(nav_history) > 0:
                    show_nav_tree()

                prompt_path = current_path.replace("A_GIS.", "")
                if prompt_path == "A_GIS":
                    prompt_text = "A_GIS> "
                else:
                    prompt_text = f"A_GIS.{prompt_path}> "

                text = session.prompt(prompt_text).strip()

                if text == "exit":
                    break
                elif text == "help":
                    console.print("\nCommands:")
                    console.print("  help  : Show this help")
                    console.print("  ..    : Go up one level")
                    console.print("  /     : Go to root")
                    console.print("  exit  : Exit explorer")
                    console.print("\nPress Enter to list contents")
                    console.print("Type component name to navigate or view details\n")
                elif text == "..":
                    if path_stack:
                        current_path = path_stack.pop()
                        current_module = importlib.import_module(current_path)
                        contents = get_module_contents(current_module)
                        completer = PathCompleter(lambda: contents)
                        nav_history.append((current_path, 'module', current_module))
                        show_contents(contents)
                elif text == "/" or text == "":
                    if text == "/":
                        path_stack = []
                        current_path = "A_GIS"
                        current_module = A_GIS
                        contents = get_module_contents(current_module)
                        completer = PathCompleter(lambda: contents)
                        nav_history.append((current_path, 'module', current_module))
                    show_contents(contents)
                elif '.' in text:
                    parts = text.split('.')
                    try:
                        nav_path = current_path
                        for part in parts:
                            if part:  # Skip empty parts
                                module = importlib.import_module(nav_path)
                                contents = get_module_contents(module)
                                if part in contents:
                                    type_, obj = contents[part]
                                    if type_ == 'module':
                                        nav_path = f"{nav_path}.{part}"
                                    else:
                                        # Handle function/class display
                                        doc = inspect.getdoc(obj)
                                        nav_history.append((f"{nav_path}.{part}", type_, obj))
                                        console.print(f"\n[bold]{type_.capitalize()}: {part}[/bold]")
                                        if inspect.isfunction(obj):
                                            console.print(f"Signature: {inspect.signature(obj)}")
                                        if doc:
                                            console.print(f"\n{doc}\n")
                                        nav_path = None
                                        break

                        if nav_path:
                            # Update current state for module navigation
                            path_stack.append(current_path)
                            current_path = nav_path
                            current_module = importlib.import_module(current_path)
                            contents = get_module_contents(current_module)
                            completer = PathCompleter(lambda: contents)
                            nav_history.append((current_path, 'module', current_module))
                            console.print(f"Moved to {current_path}")
                            show_contents(contents)

                    except Exception as e:
                        if debug:
                            console.print(f"[red]Navigation error: {str(e)}[/red]")
                        continue
                elif text in contents:
                    type_, obj = contents[text]

                    if type_ == 'module':
                        doc = inspect.getdoc(obj)
                        if doc:
                            console.print(f"\nModule Description:")
                            console.print(f"{doc}")
                            console.print()

                        path_stack.append(current_path)
                        current_path = f"{current_path}.{text}"
                        nav_history.append((current_path, 'module', obj))
                        current_module = obj
                        contents = get_module_contents(current_module)
                        completer = PathCompleter(lambda: contents)
                        console.print(f"Moved to {current_path}")
                        show_contents(contents)
                    else:
                        doc = inspect.getdoc(obj)
                        nav_history.append((f"{current_path}.{text}", type_, obj))
                        console.print(f"\n[bold]{type_.capitalize()}: {text}[/bold]")
                        if inspect.isfunction(obj):
                            console.print(f"Signature: {inspect.signature(obj)}")
                        if doc:
                            console.print(f"\n{doc}\n")
                        else:
                            console.print("\nNo documentation available\n")
                else:
                    console.print(f"[red]Unknown: {text}[/red]")

            except KeyboardInterrupt:
                continue
            except EOFError:
                break
            except Exception as e:
                if debug:
                    console.print(f"[red]Error: {str(e)}[/red]")

    except Exception as e:
        if debug:
            console.print(f"[red]Error during initialization: {str(e)}[/red]")
            import traceback
            traceback.print_exc()

cli.add_command(cli_repl)

# This is always a main.
cli()
