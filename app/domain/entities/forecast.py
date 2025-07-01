from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List
import uuid


@dataclass
class ForecastPoint:
    date: date
    y: float

    def __post_init__(self):
        if not isinstance(self.y, (int, float)):  # type: ignore
            raise ValueError("Value must be a number.")
        if not self.date:
            raise ValueError("Date must not be empty.")
        if not self.y:
            raise ValueError("Value must not be empty.")
        if not isinstance(self.date, date):  # type: ignore
            raise ValueError("Date must be a date object.")


@dataclass
class Forecast:
    id: uuid.UUID = field(default_factory=uuid.uuid4)
    created_at: datetime = field(default_factory=datetime.now)
    points: List[ForecastPoint] = field(default_factory=list)
    model_version: str = "v1"

    def __post_init__(self):
        if not self.points:
            raise ValueError("Forecast must contain at least one point.")

        dates = [p.date for p in self.points]

        if len(dates) != len(set(dates)):
            raise ValueError("Forecast contains duplicate dates.")

        if dates != sorted(dates):
            raise ValueError("Forecast points must be ordered by date.")
