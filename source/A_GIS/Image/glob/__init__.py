def glob(*, paths, glob_args=["*.jpg", "*.png"]):
    """Recursively glob images into one flat list."""
    import A_GIS.File.glob
    import A_GIS.Image.open

    image_files = A_GIS.File.glob(paths=paths, glob_args=glob_args)
    images = [A_GIS.Image.open(path=str(file)) for file in image_files]
    return images, image_files
