def init(
    *,
    filename="app.log",
    format="%(asctime)s %(name)s - %(levelname)s - %(message)s",
):
    import A_GIS.Log._Log

    return A_GIS.Log._Log(filename, format)
