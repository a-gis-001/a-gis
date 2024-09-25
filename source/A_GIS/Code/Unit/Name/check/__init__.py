def check(*, name: str, unit_type: str = "function"):
    """Validate a given name against a specific unit type.

    This function checks the provided `name` against the specified
    `unit_type`. It first processes the `name` using an internal fix
    mechanism to ensure it adheres to the required format for the given
    `unit_type`. The function then returns a structured result
    indicating whether the processed name matches the original name.
    This result is encoded within an instance of a data class created by
    `A_GIS.Code.make_struct`.

    Args:
        name (str):
            The name to be validated.
        unit_type (str, optional):
            The type of unit for which the name is being validated.
            Defaults to 'function'.

    Returns:
        dataclass:
            An instance of a data class with attributes as follows:

            - fixed_name (str): The processed name after applying the
              fix mechanism.
            - original_name (str): The original name provided by the
              user.
            - unit_type (str): The type of unit for which the name
              validation was performed.
            - result (bool): A boolean indicating whether the fixed
              name matches the original name.
    """
    import A_GIS.Code.Unit.Name.fix
    import A_GIS.Code.make_struct

    fixed_name = A_GIS.Code.Unit.Name.fix(name=name, unit_type=unit_type)
    return A_GIS.Code.make_struct(
        fixed_name=fixed_name,
        name=name,
        unit_type=unit_type,
        result=fixed_name == name,
    )
