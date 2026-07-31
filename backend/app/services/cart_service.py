from app.models.cart import Cart
from app.models.resolved import ResolvedOrderItem


def add_to_cart(cart: Cart, item: ResolvedOrderItem) -> Cart:
    """Append a resolved item to the cart and return the updated cart."""
    cart.items.append(item)
    return cart


def remove_from_cart(cart: Cart, item_id: str) -> tuple[Cart, bool]:
    """Remove all entries for item_id from the cart. Returns (updated_cart, found)."""
    original_len = len(cart.items)
    cart.items = [i for i in cart.items if i.menu_item.id != item_id]
    return cart, len(cart.items) < original_len
