import pathlib
import typing


def read(*, source: typing.Union[str, pathlib.Path]) -> typing.Dict[str, typing.Any]:
    """
    Reads JSON data from a string or file and returns its contents as a dictionary.

    This function accepts either a JSON string or a file path encapsulated in a `pathlib.Path` object.
    It attempts to parse the input into a dictionary. If the input is a `pathlib.Path` object, it reads
    the file located at that path. If the input is a string, it is treated as JSON data.

    Args:
        source: A string representing JSON data or a `pathlib.Path` object representing the file path
                to a JSON file.

    Returns:
        A dictionary representing the parsed JSON.

    Raises:
        json.JSONDecodeError: If the input string is not a valid JSON.
        FileNotFoundError: If the specified file in `pathlib.Path` does not exist.
        IOError: For issues related to file reading.
        TypeError: If the input is neither a string nor a `pathlib.Path` object.

    Example:
        data = read(source=pathlib.Path('path/to/your/file.json'))
        # or
        data = read(source='{"key": "value"}')
    """
    import json

    if isinstance(source, pathlib.Path):
        with open(source, "r") as file:
            return json.load(file)
    else:
        return json.loads(source)
