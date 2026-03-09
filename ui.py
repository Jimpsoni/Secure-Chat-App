# prompt_toolkit 
from prompt_toolkit.application import Application
from prompt_toolkit.layout import Layout, HSplit
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.widgets import TextArea

# Event handler
from events import bus


# Other
import asyncio


messages = []

"""
Hold all the CLI related code here.
"""

chat_window = TextArea(
    text="",
    scrollbar=True,
    wrap_lines=True,
    focusable=False,
)

input_field = TextArea(
    height=1,
    prompt=">: ",
    multiline=False,
)

layout = Layout(
    HSplit([
        chat_window,
        input_field,
    ])
)

kb = KeyBindings()

app = Application(
    layout=layout,
    key_bindings=kb,
)


def new_message(msg):
    messages.append("Peer: " + msg)
    refresh_chat()
    app.invalidate()  # trigger redraw


def refresh_chat():
    chat_window.text = "\n".join(messages)


async def handle_message(text):
    bus.dispatch("outgoing_message", text)
    messages.append(f"You: {text}")
    refresh_chat()


@kb.add("enter")
def send(event):
    text = input_field.text
    input_field.text = ""
    asyncio.create_task(handle_message(text))
    event.app.invalidate()


async def main():
    await app.run_async()


# Subscribe to the "message_received" event to update the chat window when a new message is received
bus.subscribe("message_received", new_message)
