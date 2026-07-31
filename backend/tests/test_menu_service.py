import pytest

from app.models.menu import MenuItem
from app.services.menu_service import search_menu


@pytest.fixture
def menu() -> list[MenuItem]:
    return [
        MenuItem(id="chicken-sandwich", name="Chicken Sandwich", price_cents=899),
        MenuItem(id="fries", name="Fries", price_cents=349),
        MenuItem(id="cola", name="Cola", price_cents=199, available=False),
    ]


class TestSearchMenu:
    def test_exact_match(self, menu):
        result = search_menu("fries", menu)
        assert result is not None
        assert result.id == "fries"

    def test_case_insensitive_match(self, menu):
        result = search_menu("chicken sandwich", menu)
        assert result is not None
        assert result.id == "chicken-sandwich"

    def test_query_mixed_case(self, menu):
        result = search_menu("FRIES", menu)
        assert result is not None
        assert result.id == "fries"

    def test_no_match_returns_none(self, menu):
        result = search_menu("burger", menu)
        assert result is None

    def test_unavailable_item_is_still_returned(self, menu):
        result = search_menu("cola", menu)
        assert result is not None
        assert result.available is False

    def test_empty_menu_returns_none(self):
        result = search_menu("fries", [])
        assert result is None

    def test_query_is_stripped(self, menu):
        result = search_menu("  fries  ", menu)
        assert result is not None
        assert result.id == "fries"

    def test_fuzzy_match_returned(self, menu):
        result = search_menu("chicken", menu)
        assert result is not None
        assert result.id == "chicken-sandwich"
