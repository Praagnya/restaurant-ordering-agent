from difflib import get_close_matches

from app.models.menu import MenuItem

_CUTOFF = 0.4


def search_menu(
    query: str,
    menu: list[MenuItem],
) -> MenuItem | None:
    """
    Return the best-matching menu item for the query using fuzzy matching.

    Tries exact match first, then falls back to difflib closest match.
    Returns None if no item meets the similarity cutoff.
    Availability is not considered here.
    """
    normalized = query.strip().lower()
    names = [item.name.lower() for item in menu]

    # exact match first
    if normalized in names:
        return menu[names.index(normalized)]

    matches = get_close_matches(normalized, names, n=1, cutoff=_CUTOFF)
    if matches:
        return menu[names.index(matches[0])]

    return None
