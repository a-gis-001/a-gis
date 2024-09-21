def make_result(**kwargs):
    """Create a dataclass instance from keyword arguments dynamically.

    This function dynamically generates a dataclass based on the provided
    keyword arguments and their types, and then returns an instance of that
    class initialized with the given values. This allows for the creation of
    custom data classes at runtime without explicitly defining them
    beforehand.

    Args:
        **kwargs (dict):
            A dictionary of keyword arguments where each key is the name of the
            dataclass field, and each value is the corresponding value to be set in
            the field, along with its type which will be used to define the field's
            type in the generated dataclass.

    Returns:
        dataclass (ResultType):
            An instance of the dynamically created dataclass with the fields
            and values specified by the keyword arguments.
            The name of the dataclass is 'Result'.
    """
    import dataclasses

    ResultType = dataclasses.make_dataclass(
        "Result", [(k, type(v)) for k, v in kwargs.items()]
    )
    return ResultType(**kwargs)
