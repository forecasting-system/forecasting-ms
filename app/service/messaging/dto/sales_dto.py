from pydantic import BaseModel, field_validator
from typing import List
from datetime import date


class SalesEntryDTO(BaseModel):
    date: date
    value: float

    @field_validator("value")
    def value_must_be_positive(cls, v):
        if v < 0:
            raise ValueError("Sales value must be non-negative")
        return v


class SalesDTO(BaseModel):
    sales: List[SalesEntryDTO]

    @field_validator("sales")
    def sales_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("Sales list must not be empty")
        return v
