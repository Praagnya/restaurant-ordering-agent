from anthropic import Anthropic
from anthropic.types import TextBlock

from app.agent.tools import TOOLS, dispatch
from app.models.cart import Cart
from app.models.menu import MenuItem

SYSTEM_MESSAGE = """\
You are a friendly ordering assistant at Pragnya Bites. \
Help the customer place their order using the available tools. \
Never invent prices, availability, or item IDs.\
"""


def run_agent(
    customer_text: str,
    client: Anthropic,
    menu: list[MenuItem],
    cart: Cart | None = None,
    messages: list | None = None,
) -> tuple[str, Cart, list]:
    """Run the ordering agent for one customer turn. Returns (response, updated_cart, updated_messages)."""
    if cart is None:
        cart = Cart()
    if messages is None:
        messages = []

    messages.append({"role": "user", "content": customer_text})

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-5",
            max_tokens=1024,
            system=SYSTEM_MESSAGE,
            tools=TOOLS,
            messages=messages,
        )

        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason == "end_turn":
            text = next(b.text for b in response.content if isinstance(b, TextBlock))
            return text, cart, messages

        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result_text, cart = dispatch(block.name, block.input, cart, menu)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result_text,
                })

        messages.append({"role": "user", "content": tool_results})
