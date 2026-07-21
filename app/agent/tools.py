from app.models.cart import Cart
from app.models.menu import MenuItem
from app.models.order import RequestedModifier
from app.models.resolved import ResolvedOrderItem
from app.services.cart_service import add_to_cart
from app.services.menu_service import search_menu

TOOLS = [
    {
        "name": "search_menu",
        "description": "Search for a menu item by name. Call this before add_to_cart to get the item ID.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The menu item name to search for",
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "add_to_cart",
        "description": "Add a menu item to the cart using its ID from search_menu.",
        "input_schema": {
            "type": "object",
            "properties": {
                "item_id": {
                    "type": "string",
                    "description": "The menu item ID returned by search_menu",
                },
                "quantity": {
                    "type": "integer",
                    "description": "Number of items to add",
                    "minimum": 1,
                },
                "modifiers": {
                    "type": "array",
                    "description": "Ingredients to add or remove",
                    "items": {
                        "type": "object",
                        "properties": {
                            "action": {"type": "string", "enum": ["add", "remove"]},
                            "name": {"type": "string"},
                        },
                        "required": ["action", "name"],
                    },
                },
            },
            "required": ["item_id", "quantity"],
        },
    },
    {
        "name": "get_cart",
        "description": "Return the current cart contents and total.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "confirm_order",
        "description": "Call this when the customer confirms they are happy with their order.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
    {
        "name": "get_full_menu",
        "description": "Return the full list of available menu items with prices. Call this when the customer asks what's on the menu or what options are available.",
        "input_schema": {
            "type": "object",
            "properties": {},
        },
    },
]


def dispatch(
    tool_name: str,
    tool_input: dict,
    cart: Cart,
    menu: list[MenuItem],
) -> tuple[str, Cart]:
    """Execute a tool call and return (result_text, updated_cart)."""
    if tool_name == "search_menu":
        item = search_menu(tool_input["query"], menu)
        if item is None:
            return f"No item found for '{tool_input['query']}'.", cart
        if not item.available:
            return f"'{item.name}' is currently unavailable.", cart
        return item.model_dump_json(), cart

    if tool_name == "add_to_cart":
        item_id = tool_input["item_id"]
        menu_item = next((m for m in menu if m.id == item_id), None)
        if menu_item is None:
            return f"Menu item ID '{item_id}' not found.", cart
        if not menu_item.available:
            return f"'{menu_item.name}' is currently unavailable.", cart
        modifiers = [
            RequestedModifier(action=m["action"], name=m["name"])
            for m in tool_input.get("modifiers", [])
        ]
        resolved_item = ResolvedOrderItem(
            menu_item=menu_item,
            quantity=tool_input["quantity"],
            modifiers=modifiers,
        )
        cart = add_to_cart(cart, resolved_item)
        return f"Added {tool_input['quantity']}x {menu_item.name} to cart.", cart

    if tool_name == "get_cart":
        if not cart.items:
            return "The cart is empty.", cart
        lines = [f"{item.quantity}x {item.menu_item.name}" for item in cart.items]
        return f"Cart: {', '.join(lines)}. Total: ${cart.total_cents / 100:.2f}.", cart

    if tool_name == "confirm_order":
        return "Order confirmed.", cart

    if tool_name == "get_full_menu":
        lines = [
            f"{item.name} (${item.price_cents / 100:.2f})"
            for item in menu
            if item.available
        ]
        return "\n".join(lines), cart

    raise ValueError(f"Unknown tool: {tool_name}")
