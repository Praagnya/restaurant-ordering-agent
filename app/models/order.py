from typing import Literal

from pydantic import BaseModel, Field, field_validator


class RequestedModifier(BaseModel):
    action: Literal["add", "remove"]
    name: str

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, v: str) -> str:
        return v.strip().lower()


class RequestedItem(BaseModel):
    name: str = Field(min_length=1)
    quantity: int = Field(default=1, ge=1)
    modifiers: list[RequestedModifier] = Field(default_factory=list)

    @field_validator("name", mode="before")
    @classmethod
    def normalize_name(cls, v: str) -> str:
        return v.strip().lower()


class ParsedOrder(BaseModel):
    items: list[RequestedItem] = Field(default_factory=list)
