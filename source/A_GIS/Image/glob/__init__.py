def glob(*, paths, glob_args=["*.jpg", "*.png"]):
    """Recursively glob images into one flat list."""
    import A_GIS.File.glob
    import A_GIS.Image.open
    import A_GIS.Code.make_struct

    image_files = A_GIS.File.glob(paths=paths, glob_args=glob_args).files
    images = [A_GIS.Image.open(path=str(file)) for file in image_files]
    return A_GIS.Code.make_struct(images=images, files=image_files,_paths=paths,_glob_args=glob_args)
