import json
from pathlib import Path

from app.models.menu import MenuItem

MENU: list[MenuItem] = [
    # Burgers
    MenuItem(
        id="big-mac",
        name="Big Mac",
        description="Two beef patties, special sauce, lettuce, cheese, pickles, onions on a sesame bun.",
        price_cents=599,
    ),
    MenuItem(
        id="quarter-pounder",
        name="Quarter Pounder",
        description="Quarter pound beef patty with cheese, pickles, onions, ketchup and mustard.",
        price_cents=649,
    ),
    MenuItem(
        id="mcdouble",
        name="McDouble",
        description="Two beef patties with cheese, pickles, onions, ketchup and mustard.",
        price_cents=299,
    ),
    MenuItem(
        id="cheeseburger",
        name="Cheeseburger",
        description="Beef patty with cheese, pickles, onions, ketchup and mustard.",
        price_cents=199,
    ),

    # Chicken
    MenuItem(
        id="mcchicken",
        name="McChicken",
        description="Crispy chicken patty with mayo and shredded lettuce.",
        price_cents=199,
    ),
    MenuItem(
        id="crispy-chicken-sandwich",
        name="Crispy Chicken Sandwich",
        description="Crispy chicken fillet with crinkle-cut pickles and butter on a toasted bun.",
        price_cents=549,
    ),
    MenuItem(
        id="mcnuggets-6pc",
        name="McNuggets 6 Piece",
        description="6 tender chicken McNuggets.",
        price_cents=349,
    ),
    MenuItem(
        id="mcnuggets-10pc",
        name="McNuggets 10 Piece",
        description="10 tender chicken McNuggets.",
        price_cents=549,
    ),

    # Sides
    MenuItem(
        id="fries-small",
        name="Small Fries",
        description="World famous golden fries, small size.",
        price_cents=199,
    ),
    MenuItem(
        id="fries-medium",
        name="Medium Fries",
        description="World famous golden fries, medium size.",
        price_cents=299,
    ),
    MenuItem(
        id="fries-large",
        name="Large Fries",
        description="World famous golden fries, large size.",
        price_cents=349,
    ),
    MenuItem(
        id="apple-slices",
        name="Apple Slices",
        description="Fresh apple slices.",
        price_cents=99,
    ),

    # Drinks
    MenuItem(
        id="coke-medium",
        name="Medium Coke",
        description="Medium Coca-Cola.",
        price_cents=149,
    ),
    MenuItem(
        id="diet-coke-medium",
        name="Medium Diet Coke",
        description="Medium Diet Coca-Cola.",
        price_cents=149,
    ),
    MenuItem(
        id="sprite-medium",
        name="Medium Sprite",
        description="Medium Sprite.",
        price_cents=149,
    ),
    MenuItem(
        id="water",
        name="Water",
        description="Bottled water.",
        price_cents=99,
    ),

    # Desserts
    MenuItem(
        id="mcflurry-oreo",
        name="Oreo McFlurry",
        description="Vanilla soft serve blended with Oreo cookie pieces.",
        price_cents=399,
    ),
    MenuItem(
        id="apple-pie",
        name="Apple Pie",
        description="Warm baked apple pie.",
        price_cents=149,
    ),
]


def get_menu() -> list[MenuItem]:
    """Return the full in-memory menu."""
    return MENU


def get_menu_from_file(path: str = "data/menu.json") -> list[MenuItem]:
    """Load menu from a JSON file produced by scripts/parse_menu.py."""
    data = json.loads(Path(path).read_text())
    return [MenuItem(**item) for item in data]
