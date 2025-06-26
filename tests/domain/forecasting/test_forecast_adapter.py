import pytest
import pandas as pd
from datetime import datetime

from app.domain.entities.forecast import Forecast, ForecastPoint
from app.domain.forecasting.forecast_adapter import forecast_adapter


def test_forecast_adapter_valid_input():
    data = {
        'ds': [datetime(2024, 1, 1), datetime(2024, 1, 2), datetime(2024, 1, 3)],
        'yhat': [100.0, 200.0, 300.0],
        'extra': [1, 2, 3]
    }
    df = pd.DataFrame(data)
    result = forecast_adapter(df)

    assert isinstance(result, Forecast)
    assert len(result.points) == 3
    assert result.points[0] == ForecastPoint(
        date=data['ds'][0].date(), y=100.0)


def test_forecast_adapter_missing_columns():
    df = pd.DataFrame({'yhat': [1.0, 2.0]})
    with pytest.raises(ValueError, match="Forecast DataFrame must contain 'ds' and 'yhat' columns."):
        forecast_adapter(df)


def test_forecast_adapter_with_nulls():
    data = {
        'ds': [datetime(2024, 1, 1), None, datetime(2024, 1, 3)],
        'yhat': [100.0, 200.0, None]
    }
    df = pd.DataFrame(data)
    result = forecast_adapter(df)

    assert len(result.points) == 1
    assert result.points[0].date == datetime(2024, 1, 1).date()
    assert result.points[0].y == 100.0


def test_forecast_adapter_with_unordered_dates():
    data = {
        'ds': [datetime(2024, 1, 3), datetime(2024, 1, 1), datetime(2024, 1, 2)],
        'yhat': [300.0, 100.0, 200.0]
    }
    df = pd.DataFrame(data)
    with pytest.raises(ValueError, match="Forecast points must be ordered by date."):
        forecast_adapter(df)


def test_forecast_adapter_with_duplicate_dates():
    data = {
        'ds': [datetime(2024, 1, 1), datetime(2024, 1, 1), datetime(2024, 1, 2)],
        'yhat': [100.0, 150.0, 200.0]
    }
    df = pd.DataFrame(data)
    with pytest.raises(ValueError, match="Forecast contains duplicate dates."):
        forecast_adapter(df)
