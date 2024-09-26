import A_GIS.Log.track_function

@A_GIS.Log.track_function
def move(*, file: str, dest: str, __tracking_hash=None):
    """Move a file within the STACKS system while handling conflicts.

    The `move` function takes two mandatory parameters, `file` and
    `dest`, which define the source and destination paths for the file
    movement operation. It optionally accepts a `__tracking_hash`
    parameter for internal logging purposes. The function ensures that
    the file exists within the STACKS root directory and that the
    destination is also within the same root. It classifies the
    destination, ensures that no files with the same name exist at the
    destination, and then moves the file accordingly.

    The function performs the following steps:

    1. Validates the existence of the source file within the STACKS
       root directory.
    2. Validates that both the source file and the destination are
       inside the same STACKS root directory.
    3. Creates the destination if it does not already exist.
    4. Classifies the destination, handling different types of
       classifications ("leaf", "branch", or "root").
    5. Generates a unique filename for the destination if necessary,
       to avoid overwriting existing files.
    6. Moves the source file to the new destination while creating
       any required subdirectories.
    7. Optionally generates a purpose for the directory containing
       the new file.

    On failure, the function catches exceptions and returns an error
    message along with the original file, destination, and new
    destination paths. If the operation is successful, it returns a
    struct with the error set to `None`, the destination path, the new
    destination path, the original file path, and the new file path, as
    well as the classification of the destination.

    Args:
        file (str):
            The path to the file that is to be moved.
        dest (str):
            The path to the destination directory where the file will be
            moved.
        __tracking_hash (hash, optional):
            A hash value used for tracking purposes within the logging
            system.

    Returns:
        dataclass:
            With the following attributes

            - error (str): A string describing any error encountered
              during the operation or `None` if no error occurred.
            - dest (str): The path to the destination directory where
              the file was moved to.
            - new_dest (str): The full path to the new destination
              file after moving.
            - file (str): The original path of the file before it was
              moved.
            - new_file (str): The full path to the file after it was
              moved.
            - classify (str): The classification of the destination
              directory ('leaf', 'branch', or 'root').
    """
    import pathlib
    import A_GIS.File.Node.classify
    import A_GIS.File.Node.generate_purpose
    import A_GIS.File.Node.generate_dirname
    import A_GIS.File.guess_year
    import os

    # Initialize outputs.
    error = None
    file = pathlib.Path(file).resolve()
    dest = pathlib.Path(dest).resolve()
    new_file = None
    new_dest = None
    classification = None

    try:
        # Error if file doesn't exist.
        if not file.exists():
            raise ValueError(f"Error: input file {file} does not exist")

        # Error if file and dest are not inside the STACKS root.
        root = A_GIS.File.Node.get_root(path=dest).root
        if not file.is_relative_to(root):
            raise ValueError(
                f"Error: file {file} must be inside STACKS root {root}!"
            )
        if not dest.is_relative_to(root):
            raise ValueError(
                f"Error: destination {dest} must be inside STACKS root {root}!"
            )
        inbox = pathlib.Path(root) / "_inbox"
        if dest.is_relative_to(inbox):
            raise ValueError(
                f"Error: destination {dest} cannot be inside the inbox {inbox}"
            )

        # Create destination.
        if not dest.exists():
            os.makedirs(dest)

        # Classify the destination.
        classify = A_GIS.File.Node.classify(directory=str(dest))
        classification = classify.result

        if classification is None:
            raise ValueError(
                f"File {file} cannot be classified as leaf, branch, or root in the STACKS system."
            )
        elif classification == "root":
            raise ValueError(
                f"Will not move {file} to root directory {dest}! Find a fitting subdirectory."
            )
        else:
            dest_file = file.name.replace(" ", "_")
            new_dest = dest
            new_file = dest / dest_file

            if classification == "leaf":
                # If the destination is a leaf we have to make sure we don't
                # overwrite a file.
                i = 0
                while new_file.exists():
                    i += 1
                    dest_file = dest_file.stem + f"_{i}" + dest_file.suffix
                    new_file = new_dest / dest_file

            else:
                # We need to generate a subdirectory.
                year = A_GIS.File.guess_year(file=str(file)).year
                content = A_GIS.File.read_to_text(
                    path=str(file), beginchar=0, endchar=999
                ).text
                dirname = A_GIS.File.Node.generate_dirname(
                    message=f"Generate a short subdirectory name inside directory {dest} "
                    + "to contain a file named {str(file)} with first 1000 characters: {content}",
                    prefix=year + "-",
                ).dirname

                # Create a new destination.
                new_dest = dest / dirname
                if not new_dest.exists():
                    os.makedirs(new_dest)

                new_file = new_dest / dest_file

            os.rename(file, new_file)
            A_GIS.File.Node.generate_purpose(
                directory=str(new_file.parent), overwrite_existing=True
            )

    except Exception as e:
        error = str(e)

    return A_GIS.Code.make_struct(
        error=error,
        dest=str(dest),
        new_dest=str(new_dest),
        file=str(file),
        new_file=str(new_file),
        classify=classification,
    )
