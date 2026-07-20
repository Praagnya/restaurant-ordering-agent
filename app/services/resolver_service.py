from app.models.menu import MenuItem
from app.models.order import ParsedOrder, RequestedItem
from app.models.resolved import ItemResolutionResult, ResolvedOrderItem
from app.services.menu_service import search_menu


def resolve_item(
    requested_item: RequestedItem,
    menu: list[MenuItem],
) -> ItemResolutionResult:
    menu_item = search_menu(
        query=requested_item.name,
        menu=menu,
    )

    if menu_item is None:
        return ItemResolutionResult(
            status="not_found",
            requested_item=requested_item,
        )

    if not menu_item.available:
        return ItemResolutionResult(
            status="unavailable",
            requested_item=requested_item,
        )

    resolved_item = ResolvedOrderItem(
        menu_item=menu_item,
        quantity=requested_item.quantity,
        modifiers=requested_item.modifiers,
    )

    return ItemResolutionResult(
        status="resolved",
        requested_item=requested_item,
        resolved_item=resolved_item,
    )


def resolve_order(
    parsed_order: ParsedOrder,
    menu: list[MenuItem],
) -> list[ItemResolutionResult]:
    """Resolve every item in a ParsedOrder against the menu deterministically."""
    return [resolve_item(item, menu) for item in parsed_order.items]
