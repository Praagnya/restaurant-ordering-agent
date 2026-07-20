from pydantic import BaseModel, Field


class MenuItem(BaseModel):
    id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    description: str = ""
    price_cents: int = Field(ge=0)
    available: bool = True
