def calculate_embedding(
    *,
    code: str = None,
    name: str = None,
    compare: list[str] = [],
    model: str = "microsoft/graphcodebert-base",
):
    """Calculate embeddings of code."""
    import A_GIS.Code.Unit._process_args_name_code
    import A_GIS.Code.calculate_embedding
    import A_GIS.Code.Unit.read

    name, code = A_GIS.Code.Unit._process_args_name_code(name=name, code=code)

    expanded_compare=[]
    for r in compare:
        if r.startswith('A_GIS.'):
            x = A_GIS.Code.Unit.read(name=r).code
            expanded_compare.append(x)
        else:
            expanded_compare.append(r)

    y = A_GIS.Code.calculate_embedding(model=model,code=code,compare=expanded_compare)
    setattr(y, "_expanded_compare", y._compare)
    setattr(y, "_name", name)
    setattr(y, "_compare", compare)
    return y

