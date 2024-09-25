def delete(*, duplicates):
    """Delete duplicate files.

    Duplicates are calculated by A_GIS.File.Duplicates.delete.

    """
    deleted = []
    for k, v in duplicates.items():
        v = sorted(v, key=lambda x: len(os.path.basename(x)))[1:]
        for l in v:
            deleted.append(l)
            os.remove(l)

    return deleted
