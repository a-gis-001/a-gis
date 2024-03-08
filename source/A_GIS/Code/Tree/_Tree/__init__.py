import dataclasses

@dataclasses.dataclass
class _Tree:
    _type: str
    file: str
    name: str
    full_name: str
    body: str
    children: dict[str, type["_Tree"]]

    def __repr__(self):
        import A_GIS.Code.Tree.to_string

        return A_GIS.Code.Tree.to_string(tree=self)

    def to_string(self, indent_chars: str = "    ", indent: int = 0):
        import A_GIS.Code.Tree.to_string

        return A_GIS.Code.Tree.to_string(
            tree=self, indent_chars=indent_chars, indent=indent
        )

    def to_json(self):
        import A_GIS.Code.Tree.to_json

        return A_GIS.Code.Tree.to_json(tree=self)
