def distill(*, console, names: list[str]):
    """Distill a single file and register in _EGIS

    Requires a console from the command line.
    """
    import A_GIS.Text.hash
    import A_GIS.Cli.get_name_and_path
    import A_GIS.File.read
    import A_GIS.Code.find_root
    import A_GIS.File.touch
    import A_GIS.File.write
    import rich

    def count_a(text: str) -> int:
        # Pattern to match `A_GIS.` that is not inside backticks or double quotes
        # This regex is simplified for demonstration and might need adjustments
        # for edge cases
        import re

        pattern = r"""
            (?<!`)           # Negative lookbehind for `
            \bA_GIS\.        # Literal 'A_GIS.' word boundary ensures we don't start mid-identifier
            (?![^`]*`|[^"]*")  # Negative lookahead for closing ` or " without opening ones before our match
        """

        # Exclude matches within string literals
        string_pattern = r'"[^"]*?\bA_GIS\.[^"]*?"'

        # Find all potential A_GIS. instances
        potential_matches = re.findall(pattern, text, re.VERBOSE)

        # Find all string literal matches
        string_literal_matches = re.findall(string_pattern, text)

        # Exclude string literal matches from the total count
        total_exclusions = sum(
            match.count("A_GIS.") for match in string_literal_matches
        )

        return len(potential_matches) - total_exclusions

    def create_registry(names):
        registry = {}
        for name in names:

            # Get the name and path.
            name, path = A_GIS.Cli.get_name_and_path(arg=name)
            # console.print(f"Distilling unit name={name} at path={path} ...")
            flat_name = name.replace("A_GIS.", "").replace(".", "_o_")

            # Generate the distilled file.
            code = A_GIS.File.read(file=path)

            if A_GIS.Code.is_package(code=code):
                continue
            console.print("x: " + name)
            code = code.replace(
                f'def {name.split(".")[-1]}', f"def {flat_name}"
            )
            distilled_code = A_GIS.Code.distill(code=code)
            hash = A_GIS.Text.hash(text=distilled_code)
            registry[flat_name] = {
                "hash": hash,
                "code": distilled_code,
                "name": name,
                "path": path,
                "count": count_a(distilled_code),
            }

        return registry

    def update_registry(registry):
        # Sort registry items by 'count' within each sub-dict
        sorted_items = sorted(registry.items(), key=lambda x: x[1]["count"])

        # Update each item based on sorted order
        for k, v in sorted_items:

            if v["count"] == 0:
                v["count"] = -1  # This marks the item as processed
                # console.print('hash=' + v['hash'])
                # console.print(v['code'])
                # console.print('---')
                v["hash"] = A_GIS.Text.hash(text=v["code"])
                v["_egis"] = "_EGIS.sha256_" + v["hash"] + "." + k

                # Replace occurrences in other items
                for k2, v2 in registry.items():
                    if k2 != k:
                        v2["code"] = v2["code"].replace(v["name"], v["_egis"])
                        v2["count"] = count_a(v2["code"])

        # Recalculate total_count based on updated counts
        return sum(v["count"] for k, v in registry.items() if v["count"] > 0)

    registry = create_registry(names)

    # Iteratively replace all A_GIS with _EGIS
    max_iter = 10
    for iteration in range(max_iter):
        remaining = update_registry(registry)
        for k, v in registry.items():
            console.print(f'{iteration} {v["name"]} {v["count"]}')
            # console.print(v['code'])
        if remaining == 0:
            break

    # Output to _EGIS
    for k, v in registry.items():
        panel = rich.panel.Panel(
            v["code"],
            title=f"{v['hash']}",
            expand=True,
            border_style="bold cyan",
        )
        # console.print(panel)

        # Write the distilled file.
        file = (
            A_GIS.Code.find_root(path=v["path"])
            / ".."
            / "_EGIS"
            / ("sha256_" + v["hash"])
            / "__init__.py"
        )
        file = file.resolve()
        console.print(f"Writing distilled code to {file}")
        A_GIS.File.touch(path=file)
        A_GIS.File.write(content=v["code"], file=file)
