import pandas as pd
from app.domain.forecasting.model import forecast


def test_forecast(a_valid_dataset: pd.DataFrame):
    periods = 6
    initial_rows = len(a_valid_dataset)

    result = forecast(a_valid_dataset, periods=periods)

    # Check result is not None and is a DataFrame
    assert result is not None
    assert isinstance(result, pd.DataFrame)

    # Check it has more rows than the input (because of the forecast)
    assert len(result) == initial_rows + periods

    # Check for expected columns from Prophet
    expected_cols = {"ds", "yhat", "yhat_lower", "yhat_upper"}
    assert expected_cols.issubset(result.columns)

    # Ensure last date is in the future relative to input
    last_input_date = a_valid_dataset["ds"].max()
    last_forecast_date = result["ds"].max()
    assert last_forecast_date > last_input_date
