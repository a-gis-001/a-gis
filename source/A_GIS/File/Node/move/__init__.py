import A_GIS.Log.track_function

@A_GIS.Log.track_function
def move(*,file:str,dest:str):
    """Move a file"""
    import pathlib
    import A_GIS.File.Node.classify
    import A_GIS.File.Node.generate_purpose
    import A_GIS.File.Node.generate_dirname
    import A_GIS.File.guess_year

    file=pathlib.Path(file).resolve()
    dest=pathlib.Path(dest).resolve()

    classify = A_GIS.File.Node.classify(directory=str(dest))
    error=""
    if classify.result=="root":
        error=f"Will not move {file} to root directory {dest}! Find a fitting subdirectory."
    else:
        if classify.result=="leaf":
            os.move(file,dest)
        elif classify.result=="branch":
            year = A_GIS.File.guess_year(file=file).year
            dirname = A_GIS.File.Node.generate_dirname(file=file,prefix=year+'-').dirname
            dest = dest/dirname
            os.makedirs(dest)
            os.move(file,dest)
        else:
            error=f"{file} is not in a STACKS directory!"

        if error == "":
            A_GIS.File.Node.generate_purpose(directory=dest)

    return A_GIS.Code.make_struct(error=error,dest=str(dest),file=str(file),classify=classify.result)


