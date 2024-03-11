def to_json(*, tree: type["A_GIS.Code.Tree._Tree"], indent: int = 4):
    """Converts a tree object to JSON format string representation.

    This function takes a `Tree` object and an optional indentation level, converts the
    tree into a dictionary using `dataclasses.asdict()`, and then serializes this
    dictionary into a JSON-formatted string using `json.dumps()`. The `default` argument
    in `json.dumps()` is set to convert non-serializable objects (like class instances)
    to their string representation.

    Args:
        tree (Tree): A `Tree` object to be converted into a JSON-formatted string.
        indent (int, optional): The number of spaces to use for indentation in the
                                 output JSON string. Defaults to 4.

    Raises:
        None

    Returns:
        str: A JSON-formatted string representing the tree object.
    """

    import json
    import dataclasses

    return json.dumps(
        dataclasses.asdict(tree), default=lambda o: str(o), indent=indent
    )
