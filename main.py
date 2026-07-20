import os
import sys

from dotenv import load_dotenv
from anthropic import Anthropic

from app.agent.parser import parse_order
# from app.repositories.menu import get_menu
# from app.services.resolver_service import resolve_order


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
    # menu = get_menu()

    order = parse_order(customer_text, client)
    print(order)

    # results = resolve_order(order, menu)

    # total_cents = 0
    # for r in results:
    #     if r.status == "resolved":
    #         item = r.resolved_item
    #         line_cents = item.menu_item.price_cents * item.quantity
    #         total_cents += line_cents
    #         mods = ", ".join(f"{m.action} {m.name}" for m in item.modifiers)
    #         mod_str = f"  ({mods})" if mods else ""
    #         print(f"  {item.quantity}x  {item.menu_item.name}{mod_str}  ${line_cents / 100:.2f}")
    #     elif r.status == "not_found":
    #         print(f"  --  '{r.requested_item.name}' not found on menu")
    #     elif r.status == "unavailable":
    #         print(f"  --  '{r.requested_item.name}' is currently unavailable")

    # print(f"\nTotal: ${total_cents / 100:.2f}")


if __name__ == "__main__":
    main()
