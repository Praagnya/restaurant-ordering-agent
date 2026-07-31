import pytest
from pydantic import ValidationError

from app.models.menu import MenuItem


class TestMenuItem:
    def test_valid_item(self):
        item = MenuItem(id="chicken-sandwich", name="Chicken Sandwich", price_cents=899)
        assert item.id == "chicken-sandwich"
        assert item.name == "Chicken Sandwich"
        assert item.price_cents == 899
        assert item.available is True
        assert item.description == ""

    def test_with_description(self):
        item = MenuItem(
            id="chicken-sandwich",
            name="Chicken Sandwich",
            description="Crispy fried chicken on a brioche bun",
            price_cents=899,
        )
        assert item.description == "Crispy fried chicken on a brioche bun"

    def test_free_item(self):
        item = MenuItem(id="water", name="Water", price_cents=0)
        assert item.price_cents == 0

    def test_unavailable_item(self):
        item = MenuItem(id="special", name="Daily Special", price_cents=1200, available=False)
        assert item.available is False

    def test_negative_price_rejected(self):
        with pytest.raises(ValidationError):
            MenuItem(id="burger", name="Burger", price_cents=-1)

    def test_empty_id_rejected(self):
        with pytest.raises(ValidationError):
            MenuItem(id="", name="Burger", price_cents=500)

    def test_empty_name_rejected(self):
        with pytest.raises(ValidationError):
            MenuItem(id="burger", name="", price_cents=500)

    def test_missing_id_rejected(self):
        with pytest.raises(ValidationError):
            MenuItem(name="Burger", price_cents=500)

    def test_missing_price_rejected(self):
        with pytest.raises(ValidationError):
            MenuItem(id="burger", name="Burger")
