import pytest
from datetime import date
from pydantic import ValidationError

from app.service.messaging.dto.sales_dto import SalesDTO

# --- Valid case ---


def test_valid_sales_dto():
    data = {
        "sales": [
            {"date": "2024-01-01", "value": 100.0},
            {"date": "2024-01-02", "value": 150.0}
        ]
    }
    dto = SalesDTO(**data)
    assert len(dto.sales) == 2
    assert dto.sales[0].date == date(2024, 1, 1)
    assert dto.sales[1].value == 150.0

# --- Empty sales list ---


def test_sales_dto_empty_sales_list():
    data = {
        "sales": []
    }
    with pytest.raises(ValidationError) as exc:
        SalesDTO(**data)
    assert "Sales list must not be empty" in str(exc.value)

# --- Negative value ---


def test_sales_entry_dto_negative_value():
    data = {
        "sales": [
            {"date": "2024-01-01", "value": -10.0}
        ]
    }
    with pytest.raises(ValidationError) as exc:
        SalesDTO(**data)
    assert "Sales value must be non-negative" in str(exc.value)
