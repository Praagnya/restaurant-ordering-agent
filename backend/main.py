import os
import sys

from dotenv import load_dotenv
from anthropic import Anthropic

from app.agent.agent import run_agent
from app.models.cart import Cart
from app.repositories.menu import get_menu


def main() -> None:
    load_dotenv()
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set in environment or .env")
        sys.exit(1)

    client = Anthropic(api_key=api_key)
    menu = get_menu()

    cart = Cart()
    messages = []

    print("Welcome to Pragnya Bites! What would you like to order? (type 'quit' to exit)\n")

    while True:
        customer_text = input("You: ").strip()
        if not customer_text:
            continue
        if customer_text.lower() in ("quit", "exit"):
            break

        response, cart, messages = run_agent(customer_text, client, menu, cart, messages)
        print(f"\nAgent: {response}\n")


if __name__ == "__main__":
    main()
