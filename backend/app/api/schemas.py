from pydantic import BaseModel

from app.models.cart import Cart
from app.models.menu import MenuItem


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str


class ChatResponse(BaseModel):
    session_id: str
    response: str
    cart: Cart


class MenuParseResponse(BaseModel):
    restaurant_name: str
    section_count: int
    items: list[MenuItem]
