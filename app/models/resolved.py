from typing import Literal

from pydantic import BaseModel, Field

from app.models.menu import MenuItem
from app.models.order import RequestedItem, RequestedModifier


class ResolvedOrderItem(BaseModel):
    menu_item: MenuItem
    quantity: int = Field(ge=1)
    modifiers: list[RequestedModifier] = Field(default_factory=list)


class ItemResolutionResult(BaseModel):
    status: Literal["resolved", "not_found", "unavailable"]
    requested_item: RequestedItem
    resolved_item: ResolvedOrderItem | None = None
