import pytest

from app.models.menu import MenuItem
from app.models.order import ParsedOrder, RequestedItem, RequestedModifier
from app.services.resolver_service import resolve_item, resolve_order


@pytest.fixture
def menu() -> list[MenuItem]:
    return [
        MenuItem(id="chicken-sandwich", name="Chicken Sandwich", price_cents=899),
        MenuItem(id="fries", name="Fries", price_cents=349),
        MenuItem(id="cola", name="Cola", price_cents=199, available=False),
    ]


class TestResolveItem:
    def test_found_item_returns_resolved_status(self, menu):
        result = resolve_item(RequestedItem(name="fries"), menu)
        assert result.status == "resolved"

    def test_resolved_item_contains_correct_menu_item(self, menu):
        result = resolve_item(RequestedItem(name="fries"), menu)
        assert result.resolved_item is not None
        assert result.resolved_item.menu_item.id == "fries"

    def test_quantity_preserved(self, menu):
        result = resolve_item(RequestedItem(name="fries", quantity=3), menu)
        assert result.resolved_item is not None
        assert result.resolved_item.quantity == 3

    def test_modifiers_preserved(self, menu):
        item = RequestedItem(
            name="chicken sandwich",
            modifiers=[RequestedModifier(action="remove", name="onions")],
        )
        result = resolve_item(item, menu)
        assert result.resolved_item is not None
        assert len(result.resolved_item.modifiers) == 1
        assert result.resolved_item.modifiers[0].name == "onions"

    def test_requested_item_preserved_on_resolved(self, menu):
        requested = RequestedItem(name="fries")
        result = resolve_item(requested, menu)
        assert result.requested_item.name == "fries"

    def test_item_not_found_returns_not_found_status(self, menu):
        result = resolve_item(RequestedItem(name="burger"), menu)
        assert result.status == "not_found"

    def test_not_found_has_no_resolved_item(self, menu):
        result = resolve_item(RequestedItem(name="burger"), menu)
        assert result.resolved_item is None

    def test_unavailable_item_returns_unavailable_status(self, menu):
        result = resolve_item(RequestedItem(name="cola"), menu)
        assert result.status == "unavailable"

    def test_unavailable_has_no_resolved_item(self, menu):
        result = resolve_item(RequestedItem(name="cola"), menu)
        assert result.resolved_item is None

    def test_requested_item_preserved_on_not_found(self, menu):
        requested = RequestedItem(name="burger")
        result = resolve_item(requested, menu)
        assert result.requested_item.name == "burger"


class TestResolveOrder:
    def test_empty_order_returns_empty_list(self, menu):
        results = resolve_order(ParsedOrder(items=[]), menu)
        assert results == []

    def test_single_item_resolved(self, menu):
        order = ParsedOrder(items=[RequestedItem(name="fries")])
        results = resolve_order(order, menu)
        assert len(results) == 1
        assert results[0].status == "resolved"

    def test_multiple_items_all_resolved(self, menu):
        order = ParsedOrder(items=[
            RequestedItem(name="fries"),
            RequestedItem(name="chicken sandwich"),
        ])
        results = resolve_order(order, menu)
        assert len(results) == 2
        assert all(r.status == "resolved" for r in results)

    def test_not_found_item_in_mixed_order(self, menu):
        order = ParsedOrder(items=[
            RequestedItem(name="fries"),
            RequestedItem(name="pizza"),
        ])
        results = resolve_order(order, menu)
        assert results[0].status == "resolved"
        assert results[1].status == "not_found"

    def test_unavailable_item_in_order(self, menu):
        order = ParsedOrder(items=[RequestedItem(name="cola")])
        results = resolve_order(order, menu)
        assert results[0].status == "unavailable"

    def test_result_count_matches_item_count(self, menu):
        order = ParsedOrder(items=[
            RequestedItem(name="fries"),
            RequestedItem(name="burger"),
            RequestedItem(name="cola"),
        ])
        results = resolve_order(order, menu)
        assert len(results) == 3
