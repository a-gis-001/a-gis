def _wrap_single_block(*, code_body: str):
    import A_GIS.Code.Unit._Unit

    return A_GIS.Code.Unit._Unit(None, None, None, [code_body])
