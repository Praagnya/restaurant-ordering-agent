from anthropic import Anthropic
from anthropic.types import TextBlock
from langsmith import traceable
from langsmith.wrappers import wrap_anthropic

from app.agent.tools import TOOLS, dispatch
from app.models.cart import Cart
from app.models.menu import MenuItem

SYSTEM_MESSAGE = """\
You are a friendly voice ordering assistant at Pragnya Bites.

On the customer's first message, greet them warmly and invite them to order.

Keep the conversation natural and flowing — confirm items as they're added, \
offer to clarify options, and guide them toward completing their order. \
When they seem done, recap their cart and ask if they'd like anything else before confirming.

Use tools when you need to look up menu items, manage the cart, or confirm an order. \
For simple follow-up questions where you already know the answer from the conversation — \
like order number, cart contents, or prices already discussed — respond directly without calling a tool.

Never use markdown, bullet points, or emojis — this is voice, so speak naturally.
Never invent prices, availability, or item IDs.\
"""


@traceable(name="run_agent")
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

    client = wrap_anthropic(client)
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
