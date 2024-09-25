import A_GIS.Log.track_function

@A_GIS.Log.track_function
def move(*, file: str, dest: str):
    """Move a file within STACKS, maintaining naming conventions.

    This function moves a file to a specified destination path, ensuring
    that the operation adheres to the STACKs directory naming
    conventions based on the file's name and extension. It uses the
    `A_GIS.File.Node` module to classify the file and determine the
    appropriate subdirectory into which it should be moved. The function
    also logs the operation using `A_GIS.Log.track_function`.

    The `move` function performs the following steps:

    1. Classifies the file to determine its category (root, leaf, or
       branch).
    2. If the file is in a root directory, it prompts the user to
       select a fitting subdirectory.
    3. If the file is in a leaf directory, it simply moves the file
       to the specified destination.
    4. If the file is on a branch, it creates a new subdirectory
       within the destination path, named according to the file's
       date, and moves the file there.
    5. It generates a purpose for the moved file if no error occurs.
    6. Returns a structured result indicating whether the operation
       was successful or if an error occurred.

    Args:
        file (str):
            The path to the source file that is to be moved.
        dest (str):
            The path where the file should be moved to.

    Returns:
        dataclass:
            With the following attributes

            - error (str, optional): A message indicating any errors
              encountered during the operation or a success
              confirmation if no errors occurred.
            - dest (str): The path to the destination directory where
              the file was moved to.
            - file (str): The path to the source file that was moved.
            - classify (str): The classification result ('root',
              'leaf', or 'branch') of the source file's directory
              structure.
    """
    import pathlib
    import A_GIS.File.Node.classify
    import A_GIS.File.Node.generate_purpose
    import A_GIS.File.Node.generate_dirname
    import A_GIS.File.guess_year

    file = pathlib.Path(file).resolve()
    dest = pathlib.Path(dest).resolve()

    classify = A_GIS.File.Node.classify(directory=str(dest))
    error = ""
    if classify.result == "root":
        error = f"Will not move {file} to root directory {dest}! Find a fitting subdirectory."
    else:
        if classify.result == "leaf":
            os.move(file, dest)
        elif classify.result == "branch":
            year = A_GIS.File.guess_year(file=file).year
            dirname = A_GIS.File.Node.generate_dirname(
                file=file, prefix=year + "-"
            ).dirname
            dest = dest / dirname
            os.makedirs(dest)
            os.move(file, dest)
        else:
            error = f"{file} is not in a STACKS directory!"

        if error == "":
            A_GIS.File.Node.generate_purpose(directory=dest)

    return A_GIS.Code.make_struct(
        error=error, dest=str(dest), file=str(file), classify=classify.result
    )
