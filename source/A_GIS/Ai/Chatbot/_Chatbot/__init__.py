import dataclasses
import typing

@dataclasses.dataclass
class _Chatbot:
    """Manage state for a chatbot."""

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

    # List of messages.
    messages: list[dict]

    # Names of A_GIS.* functions to use as tools.
    tool_names: list[str]
    tools: list[dict]

    def __post_init__(self):
        """Initialize tools and messages."""
        import A_GIS.Code.get_schema

        # Add the system message.
        if len(self.messages) == 0 and self.system != "":
            self.messages = [{"role": "system", "content": self.system}]

        # Expand the tools.
        if len(self.tools) == 0:
            for tool_name in self.tool_names:
                self.tools.append(A_GIS.Code.get_schema(func_path=tool_name))

    def chat(
        self,
        *,
        message: str,
        **kwargs,
    ):
        """Forwards to send chat."""
        self.messages.append({"role": "user", "content": message})
        return self._send_chat(
            model=self.model,
            messages=self.messages,
            tools=self.tools,
            **self._get_kwargs(**kwargs),
        )

    def _get_kwargs(self, **kwargs):
        """Forwards args."""

        # List of all options that can have default values from the instance.
        options = ["mirostat", "num_predict", "num_ctx", "temperature"]

        # Update kwargs with the instance's defaults if not already specified.
        for option in options:
            if option not in kwargs:
                kwargs[option] = getattr(self, option)

        return kwargs
