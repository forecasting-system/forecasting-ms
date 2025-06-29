import pytest
from datetime import date

from app.domain.entities.forecast import Forecast, ForecastPoint


# --- Valid case ---
def test_valid_forecast():
    points = [
        ForecastPoint(date=date(2024, 1, 1), y=10.0),
        ForecastPoint(date=date(2024, 1, 2), y=20.0),
    ]
    forecast = Forecast(points=points, model_version="v1")
    assert forecast.id is not None
    assert forecast.created_at is not None
    assert len(forecast.points) == 2
    assert forecast.model_version == "v1"

# --- ForecastPoint validations ---


def test_forecast_point_invalid_date_type():
    with pytest.raises(ValueError, match="Date must be a date object."):
        ForecastPoint(date="2024-01-01", y=10.0)  # type: ignore


def test_forecast_point_invalid_y_type():
    with pytest.raises(ValueError, match="Value must be a number."):
        ForecastPoint(date=date(2024, 1, 1), y="high")  # type: ignore


def test_forecast_point_empty_date():
    with pytest.raises(ValueError, match="Date must not be empty."):
        ForecastPoint(date=None, y=10.0)  # type: ignore


def test_forecast_point_empty_y():
    with pytest.raises(ValueError, match="Value must not be empty."):
        ForecastPoint(date=date(2024, 1, 1), y=0)

# --- Forecast entity validations ---


def test_forecast_without_points():
    with pytest.raises(ValueError, match="Forecast must contain at least one point."):
        Forecast(points=[], model_version="v1")


def test_forecast_with_duplicate_dates():
    points = [
        ForecastPoint(date=date(2024, 1, 1), y=10.0),
        ForecastPoint(date=date(2024, 1, 1), y=20.0),
    ]
    with pytest.raises(ValueError, match="Forecast contains duplicate dates."):
        Forecast(points=points, model_version="v1")


def test_forecast_with_unsorted_dates():
    points = [
        ForecastPoint(date=date(2024, 1, 2), y=20.0),
        ForecastPoint(date=date(2024, 1, 1), y=10.0),
    ]
    with pytest.raises(ValueError, match="Forecast points must be ordered by date."):
        Forecast(points=points, model_version="v1")
