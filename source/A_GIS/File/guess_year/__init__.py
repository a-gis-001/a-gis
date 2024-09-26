def guess_year(*, file: str):
    """Guess the year based on a file's last modification time.

    This function infers the year associated with a file by examining
    its last modification time. It converts this timestamp to a datetime
    object and then extracts the year from it. This can be useful for
    organizing files by their creation or last modified date.

    Args:
        file (str):
            The path to the file whose year is to be guessed.

    Returns:
        dataclass:
            An instance of a dataclass with the following attributes

            - text (str): A string representation of the file's
              metadata.
            - result (str): A string representing the inferred year
              from the file's last modification time.
    """
    import A_GIS.Code.make_struct
    import A_GIS.Code.guess_name
    import os
    import datetime

    # Get the last modification time
    mod_time = os.path.getmtime(file)

    # Convert it to a datetime object
    mod_datetime = datetime.datetime.fromtimestamp(mod_time)

    return A_GIS.Code.make_struct(
        _caller=A_GIS.Code.guess_name(path=__file__),
        file=file,
        year=str(mod_datetime.year),
    )
