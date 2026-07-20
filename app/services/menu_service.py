from app.models.menu import MenuItem


def search_menu(
    query: str,
    menu: list[MenuItem],
) -> MenuItem | None:
    """
    Return the first menu item whose normalized name matches the normalized query.

    Return None when no menu item matches.

    Availability is not considered here.
    """
    normalized = query.strip().lower()
    for item in menu:
        if item.name.lower() == normalized:
            return item
    return None
