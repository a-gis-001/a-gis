import A_GIS.Log.track_function

@A_GIS.Log.track_function
def move(*, file: str, dest: str, __tracking_hash=None):
    """Move a file within the STACKS file system.

    This function moves a given file to a new destination path, handling
    different types of directories (root, leaf, and branch) and ensuring
    that the move operation does not result in overwriting existing
    files or moving files outside of STACKS-managed directories. It
    returns a structured response with the outcome of the move
    operation.

    Args:
        file (str):
            Path to the source file that needs to be moved.
        dest (str):
            Path to the destination directory where the file should be
            moved.

    Returns:
        dataclass:
            A structured object containing the following attributes:

            - error (str): An error message if an issue occurs during
              the move operation,
            otherwise an empty string indicating success.

            - dest (str): The path to the destination directory where
              the file was moved.
            - file (str): The path to the source file that was moved.
            - new_file (str): The path to the file after it has been
              moved to the new location.
            - classify (str): A classification of the destination
              directory type, which can be "root", "leaf", or
              "branch".

    Raises:
        ValueError:
            If the `dest` path is not a valid STACKS directory or if an
            attempt is made to move the file outside the STACKS
            structure.
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
