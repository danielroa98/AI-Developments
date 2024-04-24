from openai import AssistantEventHandler
from typing_extensions import override

class EventHandler(AssistantEventHandler):
    """
    Handles events triggered by the assistant.
    """

    @override
    def on_text_created(self, text) -> None:
        """
        Called when a new text is created.

        Args:
            text: The newly created text.
        """
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        """
        Called when a text delta is received.

        Args:
            delta: The text delta.
            snapshot: The current snapshot of the text.
        """
        print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        """
        Called when a new tool call is created.

        Args:
            tool_call: The newly created tool call.
        """
        print(f"\nassistant > {tool_call.type}\n", flush=True)

    def on_tool_call_delta(self, delta, snapshot):
        """
        Called when a tool call delta is received.

        Args:
            delta: The tool call delta.
            snapshot: The current snapshot of the tool call.
        """
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "logs":
                        print(f"\n{output.logs}", flush=True)
 
# Then, we use the `stream` SDK helper 
# with the `EventHandler` class to create the Run 
# and stream the response.