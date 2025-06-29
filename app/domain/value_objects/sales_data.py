from dataclasses import dataclass
from datetime import date
from typing import List


@dataclass(frozen=True)
class SalesEntry:
    date: date
    value: float

    def __post_init__(self):
        if self.value < 0:
            raise ValueError("Sales value must be non-negative.")


@dataclass(frozen=True)
class SalesData:
    entries: List[SalesEntry]

    def __post_init__(self):
        if not self.entries:
            raise ValueError("Sales data must contain at least one entry.")

        dates = [entry.date for entry in self.entries]

        if len(dates) != len(set(dates)):
            raise ValueError("Sales data contains duplicate dates.")

        if dates != sorted(dates):
            raise ValueError("Sales data entries must be sorted by date.")
