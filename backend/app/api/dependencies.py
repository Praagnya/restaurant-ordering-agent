import os
from dataclasses import dataclass, field
from functools import lru_cache

from anthropic import Anthropic
from dotenv import load_dotenv

from app.models.cart import Cart
from app.models.menu import MenuItem
from app.repositories.menu import get_menu

load_dotenv()


@lru_cache(maxsize=1)
def get_client() -> Anthropic:
    return Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])


@lru_cache(maxsize=1)
def get_menu_items() -> list[MenuItem]:
    return get_menu()


@dataclass
class Session:
    cart: Cart = field(default_factory=Cart)
    messages: list = field(default_factory=list)


# In-memory session store: session_id → Session
sessions: dict[str, Session] = {}

# Module-level aliases used by routes
client = get_client()
menu = get_menu_items()
