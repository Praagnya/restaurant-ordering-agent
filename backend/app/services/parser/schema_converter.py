import re

from app.models.menu import MenuItem


def slugify(name: str) -> str:
    """Convert item name to a URL-safe ID. 'Big Mac' → 'big-mac'."""
    slug = name.lower()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"\s+", "-", slug.strip())
    slug = re.sub(r"-+", "-", slug)
    return slug


def convert_to_menu_items(extracted: dict) -> list[MenuItem]:
    """Convert intermediate extraction dict to List[MenuItem]."""
    items = []
    seen_ids: dict[str, int] = {}

    for section in extracted.get("sections", []):
        for item in section.get("items", []):
            name = item["name"]
            base_id = slugify(name)

            # Deduplicate IDs (e.g. two items named "Special")
            if base_id in seen_ids:
                seen_ids[base_id] += 1
                item_id = f"{base_id}-{seen_ids[base_id]}"
            else:
                seen_ids[base_id] = 1
                item_id = base_id

            items.append(MenuItem(
                id=item_id,
                name=name,
                description=item.get("description") or "",
                price_cents=item.get("price_cents", 0),
                available=item.get("available", True),
            ))

    return items
