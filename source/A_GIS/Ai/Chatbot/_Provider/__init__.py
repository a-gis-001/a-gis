import enum
import typing

class _Provider:
    # Define the allowed values as class-level Literal type
    types_allowed = typing.Literal["ollama", "openai", "groq"]

    # Dynamically create an Enum inside the class.
    names_allowed = [name for name in types_allowed.__args__]
