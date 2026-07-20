import pytest
from pydantic import ValidationError

from app.models.order import ParsedOrder, RequestedItem, RequestedModifier


class TestRequestedModifier:
    def test_add_action(self):
        mod = RequestedModifier(action="add", name="cheese")
        assert mod.action == "add"
        assert mod.name == "cheese"

    def test_remove_action(self):
        mod = RequestedModifier(action="remove", name="onions")
        assert mod.action == "remove"
        assert mod.name == "onions"

    def test_invalid_action_rejected(self):
        with pytest.raises(ValidationError):
            RequestedModifier(action="without", name="onions")

    def test_missing_action_rejected(self):
        with pytest.raises(ValidationError):
            RequestedModifier(name="onions")

    def test_missing_name_rejected(self):
        with pytest.raises(ValidationError):
            RequestedModifier(action="remove")

    def test_name_lowercased(self):
        mod = RequestedModifier(action="remove", name="Onions")
        assert mod.name == "onions"

    def test_name_stripped(self):
        mod = RequestedModifier(action="add", name="  cheese  ")
        assert mod.name == "cheese"


class TestRequestedItem:
    def test_defaults(self):
        item = RequestedItem(name="fries")
        assert item.quantity == 1
        assert item.modifiers == []

    def test_explicit_quantity(self):
        item = RequestedItem(name="chicken sandwich", quantity=2)
        assert item.quantity == 2

    def test_with_modifiers(self):
        item = RequestedItem(
            name="chicken sandwich",
            quantity=1,
            modifiers=[RequestedModifier(action="remove", name="onions")],
        )
        assert len(item.modifiers) == 1
        assert item.modifiers[0].action == "remove"
        assert item.modifiers[0].name == "onions"

    def test_missing_name_rejected(self):
        with pytest.raises(ValidationError):
            RequestedItem(quantity=1)

    def test_name_lowercased(self):
        item = RequestedItem(name="Chicken Sandwich")
        assert item.name == "chicken sandwich"

    def test_name_stripped(self):
        item = RequestedItem(name="  fries  ")
        assert item.name == "fries"

    def test_whitespace_only_name_rejected(self):
        with pytest.raises(ValidationError):
            RequestedItem(name="   ")

    def test_empty_name_rejected(self):
        with pytest.raises(ValidationError):
            RequestedItem(name="", quantity=1)

    def test_zero_quantity_rejected(self):
        with pytest.raises(ValidationError):
            RequestedItem(name="fries", quantity=0)

    def test_negative_quantity_rejected(self):
        with pytest.raises(ValidationError):
            RequestedItem(name="fries", quantity=-1)

    def test_modifiers_are_independent_per_instance(self):
        item1 = RequestedItem(name="burger")
        item2 = RequestedItem(name="wrap")
        item1.modifiers.append(RequestedModifier(action="add", name="sauce"))
        assert item2.modifiers == []


class TestParsedOrder:
    def test_empty_items_is_valid(self):
        order = ParsedOrder()
        assert order.items == []

    def test_explicit_empty_items(self):
        order = ParsedOrder(items=[])
        assert order.items == []

    def test_single_item(self):
        order = ParsedOrder(items=[RequestedItem(name="fries")])
        assert len(order.items) == 1
        assert order.items[0].name == "fries"

    def test_multiple_items(self):
        order = ParsedOrder(items=[
            RequestedItem(name="big mac"),
            RequestedItem(name="medium fries", quantity=2),
        ])
        assert len(order.items) == 2

    def test_item_normalisation_applied(self):
        order = ParsedOrder(items=[RequestedItem(name="  Big Mac  ")])
        assert order.items[0].name == "big mac"

    def test_items_are_independent_per_instance(self):
        order1 = ParsedOrder()
        order2 = ParsedOrder()
        order1.items.append(RequestedItem(name="fries"))
        assert order2.items == []
