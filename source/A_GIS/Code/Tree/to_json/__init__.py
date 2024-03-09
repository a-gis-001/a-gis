def to_json(*, tree: type["A_GIS.Code.Tree._Tree"], indent: int = 4):
    import json
    import dataclasses

    return json.dumps(
        dataclasses.asdict(tree), default=lambda o: str(o), indent=indent
    )
