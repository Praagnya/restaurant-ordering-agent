from pydantic import BaseModel, Field

from app.models.resolved import ResolvedOrderItem


class Cart(BaseModel):
    items: list[ResolvedOrderItem] = Field(default_factory=list)

    @property
    def total_cents(self) -> int:
        return sum(item.menu_item.price_cents * item.quantity for item in self.items)
