import pandas as pd
from app.domain.forecasting.model import forecast
from app.domain.value_objects.sales_data import SalesEntry, SalesData
from tests.mock_data.mock_sales_data import mock_sales_data


def test_forecast():
    # DATA PREPARATION
    entries = [SalesEntry(sales_entry[0], sales_entry[1])
               for sales_entry in mock_sales_data]

    sales_data = SalesData(entries=entries)

    dates = pd.to_datetime([entry.date for entry in sales_data.entries])
    values = [entry.value for entry in sales_data.entries]

    df = pd.DataFrame({
        "ds": dates,
        "y": values
    })

    df["ds"] = df["ds"].dt.to_period("M").dt.to_timestamp()
    df.index = df["ds"]
    df.index.freq = "MS"

    # PARAMETERS
    periods = 6

    # FORECAST
    result = forecast(df, periods=periods)

    # CHECK RESULT
    # Check result is not None and is a DataFrame
    assert result is not None
    assert isinstance(result, pd.DataFrame)

    # Check it has more rows than the input (because of the forecast)
    initial_rows = len(df)
    assert len(result) == initial_rows + periods

    # Check for expected columns from Prophet
    expected_cols = {"ds", "yhat", "yhat_lower", "yhat_upper"}
    assert expected_cols.issubset(result.columns)

    # Ensure last date is in the future relative to input
    last_input_date = df["ds"].max()
    last_forecast_date = result["ds"].max()
    assert last_forecast_date > last_input_date

    first_forecast_date = result["ds"].iloc[-periods]
    assert first_forecast_date > last_input_date
