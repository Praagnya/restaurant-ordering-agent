from app.models.cart import Cart
from app.models.resolved import ResolvedOrderItem


def add_to_cart(cart: Cart, item: ResolvedOrderItem) -> Cart:
    """Append a resolved item to the cart and return the updated cart."""
    cart.items.append(item)
    return cart
