from typing import Literal

from pydantic import BaseModel, Field


class RequestedModifier(BaseModel):
    action: Literal["add", "remove"]
    name: str


class RequestedItem(BaseModel):
    name: str
    quantity: int = 1
    modifiers: list[RequestedModifier] = Field(default_factory=list)


class ParsedOrder(BaseModel):
    items: list[RequestedItem]
