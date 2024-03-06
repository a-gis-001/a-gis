import dataclasses

@dataclasses.dataclass
class _Unit:
    type_imports: list[str]
    function_definition: list[str]
    docstring: list[str]
    code_body: list[list[str]]

    def __repr__(self):
        import A_GIS.Code.Unit.to_string

        return A_GIS.Code.Unit.to_string(unit=self, start_index=0)
