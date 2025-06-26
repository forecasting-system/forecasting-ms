import pytest
from datetime import date

from app.domain.value_objects.sales_data import SalesData, SalesEntry

# --- Valid input ---


def test_valid_sales_data():
    entries = [
        SalesEntry(date=date(2024, 1, 1), value=100.0),
        SalesEntry(date=date(2024, 1, 2), value=150.0),
        SalesEntry(date=date(2024, 1, 3), value=200.0)
    ]
    sales_data = SalesData(entries=entries)
    assert len(sales_data.entries) == 3

# --- SalesEntry: negative value ---


def test_sales_entry_negative_value():
    with pytest.raises(ValueError, match="Sales value must be non-negative."):
        SalesEntry(date=date(2024, 1, 1), value=-10.0)

# --- SalesData: empty list ---


def test_sales_data_empty_list():
    with pytest.raises(ValueError, match="SalesData must contain at least one entry."):
        SalesData(entries=[])

# --- SalesData: duplicate dates ---


def test_sales_data_duplicate_dates():
    entries = [
        SalesEntry(date=date(2024, 1, 1), value=100.0),
        SalesEntry(date=date(2024, 1, 1), value=150.0)
    ]
    with pytest.raises(ValueError, match="SalesData contains duplicate dates."):
        SalesData(entries=entries)

# --- SalesData: unsorted dates ---


def test_sales_data_unsorted_dates():
    entries = [
        SalesEntry(date=date(2024, 1, 2), value=100.0),
        SalesEntry(date=date(2024, 1, 1), value=150.0)
    ]
    with pytest.raises(ValueError, match="SalesData entries must be sorted by date."):
        SalesData(entries=entries)
