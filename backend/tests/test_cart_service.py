import pytest

from app.models.cart import Cart
from app.models.menu import MenuItem
from app.models.order import RequestedModifier
from app.models.resolved import ResolvedOrderItem
from app.services.cart_service import add_to_cart

BIG_MAC = MenuItem(
    id="big-mac",
    name="Big Mac",
    description="Two beef patties.",
    price_cents=599,
)


def make_item(
    menu_item: MenuItem,
    quantity: int = 1,
    modifiers: list[RequestedModifier] | None = None,
) -> ResolvedOrderItem:
    return ResolvedOrderItem(
        menu_item=menu_item,
        quantity=quantity,
        modifiers=modifiers or [],
    )


def test_add_one_item_to_empty_cart():
    cart = Cart()
    item = make_item(BIG_MAC, quantity=2)
    cart = add_to_cart(cart, item)
    assert len(cart.items) == 1
    assert cart.items[0].quantity == 2


def test_add_multiple_items():
    cart = Cart()
    cart = add_to_cart(cart, make_item(BIG_MAC, quantity=1))
    cart = add_to_cart(cart, make_item(BIG_MAC, quantity=1))
    assert len(cart.items) == 2


def test_same_item_different_modifiers_are_separate_line_items():
    cart = Cart()
    regular = make_item(BIG_MAC, quantity=1)
    no_onions = make_item(
        BIG_MAC,
        quantity=1,
        modifiers=[RequestedModifier(action="remove", name="onions")],
    )
    cart = add_to_cart(cart, regular)
    cart = add_to_cart(cart, no_onions)
    assert len(cart.items) == 2


def test_total_cents():
    cart = Cart()
    cart = add_to_cart(cart, make_item(BIG_MAC, quantity=3))
    assert cart.total_cents == 599 * 3
