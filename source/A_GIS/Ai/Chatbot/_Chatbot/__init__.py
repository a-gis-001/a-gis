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
    _send_chat: "typing.Any"

    # Keep the state.
    messages: list[dict]

    def chat(self, message: str, *, keep_state: bool = False):
        """Chat that can keep state."""
        import A_GIS.Ai.Chatbot.chat

        # Call the main chat.
        if len(self.messages) == 0:
            self.messages = [{"role": "system", "content": self.system}]

        self.response = A_GIS.Ai.Chatbot.chat(chatbot=self, message=message)

        # Keep the state.
        if keep_state:
            self.messages.append({"role": "user", "content": message})
            self.messages.append(
                {
                    "role": "assistant",
                    "content": self.response["message"]["content"],
                }
            )

        # Return full response.
        return self.response

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
