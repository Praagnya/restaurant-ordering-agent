import json
from datetime import datetime, timezone
from pathlib import Path

from app.models.cart import Cart

ORDERS_FILE = Path("orders.json")


def save_order(cart: Cart) -> int:
    """Persist a confirmed cart to orders.json and return the order number."""
    orders = []
    if ORDERS_FILE.exists():
        orders = json.loads(ORDERS_FILE.read_text())

    order_id = len(orders) + 1

    order = {
        "id": order_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "items": [
            {
                "name": item.menu_item.name,
                "quantity": item.quantity,
                "modifiers": [{"action": m.action, "name": m.name} for m in item.modifiers],
                "line_total_cents": item.menu_item.price_cents * item.quantity,
            }
            for item in cart.items
        ],
        "total_cents": cart.total_cents,
    }

    orders.append(order)
    ORDERS_FILE.write_text(json.dumps(orders, indent=2))

    return order_id
