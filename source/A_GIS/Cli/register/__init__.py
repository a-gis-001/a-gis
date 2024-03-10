def register(func):
    """Register a function for use in the CLI

    Example usage

        @click.command()
        @A_GIS.Cli.register
        def main(module_name: str, *, methods: "show methods" = True, more: "show more including full docstring" = False):
            import importlib
            import rich

            module = importlib.import_module(module_name)
            rich.inspect(module, methods=methods, help=more)

        main()

    """
    import rich_click as click
    from functools import update_wrapper
    from inspect import signature, Parameter

    sig = signature(func)
    click_options = []
    click_arguments = []

    for name, param in sig.parameters.items():
        help_text = (
            param.annotation
            if isinstance(param.annotation, str)
            else "No description available"
        )

        if param.default is Parameter.empty:
            # Required arguments do not have default values; treated as
            # positional arguments in Click.
            click_arguments.append(click.argument(name.upper()))
        elif isinstance(param.default, bool):
            # Boolean parameters treated as flags; 'is_flag=True' and no need
            # for '--no-option' here.
            click_options.append(
                click.option(
                    f"--{name}/--no-{name}",
                    is_flag=True,
                    default=param.default,
                    show_default=True,
                    help=help_text,
                )
            )
        else:
            # Other parameters are treated as options with default values.
            click_options.append(
                click.option(
                    f"--{name}",
                    default=param.default,
                    show_default=True,
                    help=help_text,
                )
            )

    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    # Apply Click decorators in reverse order for proper stacking
    decorator_stack = click_options + click_arguments
    for decorator in reversed(decorator_stack):
        wrapper = decorator(wrapper)

    return update_wrapper(wrapper, func)
