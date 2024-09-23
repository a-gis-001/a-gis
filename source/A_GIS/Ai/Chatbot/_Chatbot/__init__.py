import dataclasses
import typing

@dataclasses.dataclass
class _Chatbot:
    # Options that could be overwritten in the chat.
    model: str
    mirostat: float
    num_predict: int
    num_ctx: int
    temperature: float

    # Options that are set by init.
    provider: str
    system: str
    keep_state: bool
    _send_chat: "typing.Any"

    # List of messages.
    messages: list[dict]

    # Names of A_GIS.* functions to use as tools.
    tool_names: list[str]
    tools: list[dict]

    def chat(self, *, message: str, **kwargs):
        """Pass through to A_GIS.Ai.Chatbot.chat."""
        import A_GIS.Ai.Chatbot.chat

        return A_GIS.Ai.Chatbot.chat(chatbot=self, message=message, **kwargs)

    def get_kwargs(self, **kwargs):
        """
        Updates the input kwargs with default values from this _Chatbot instance
        for any option not specified in the input.

        Args:
            **kwargs: Arbitrary keyword arguments.

        Returns:
            dict: Updated keyword arguments with defaults from this instance.
        """

        # List of all options that can have default values from the instance.
        options = ["mirostat", "num_predict", "num_ctx", "temperature"]

        # Update kwargs with the instance's defaults if not already specified.
        for option in options:
            if option not in kwargs:
                kwargs[option] = getattr(self, option)

        return kwargs
