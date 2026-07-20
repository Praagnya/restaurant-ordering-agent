import os
import sys

from dotenv import load_dotenv
from anthropic import Anthropic

from app.agent.parser import parse_order
from app.models.cart import Cart
from app.repositories.menu import get_menu
from app.services.cart_service import add_to_cart
from app.services.resolver_service import resolve_order


def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python main.py \"your order here\"")
        sys.exit(1)

    load_dotenv()
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set in environment or .env")
        sys.exit(1)

    customer_text = sys.argv[1]

    client = Anthropic(api_key=api_key)
    menu = get_menu()

    order = parse_order(customer_text, client)
    results = resolve_order(order, menu)

    cart = Cart()
    for r in results:
        if r.status == "resolved":
            cart = add_to_cart(cart, r.resolved_item)
        elif r.status == "not_found":
            print(f"Sorry, we don't have '{r.requested_item.name}' on our menu.")
        elif r.status == "unavailable":
            print(f"Sorry, '{r.requested_item.name}' is currently unavailable.")

    if cart.items:
        added = [f"{item.quantity}x {item.menu_item.name}" for item in cart.items]
        print(f"I've added {', '.join(added)} to your cart. \nYour total is ${cart.total_cents / 100:.2f}.")


if __name__ == "__main__":
    main()
