import pandas as pd
from prophet import Prophet


def forecast(data: pd.DataFrame, periods: int = 6) -> pd.DataFrame:
    """
    Generates a time series forecast using the Prophet model.

    Parameters:
    ----------
    data : pd.DataFrame
        A DataFrame containing historical time series data. Must meet the following requirements:
        - Columns:
            - 'ds' (datetime): Timestamps of the observations. Must be normalized to the first day of the month.
            - 'y' (float or int): Observed values to forecast.
        - The 'ds' column must be of dtype datetime64[ns], with each value representing the first day of the month
        (e.g., 2023-01-01, 2023-02-01, ...).
        - The index must match the 'ds' column and have a fixed monthly start-of-month frequency ('MS').
        - Data must be sorted chronologically (ascending by 'ds') and contain no missing months or duplicate entries.

    periods : int, default=6
        Number of future months to forecast.

    Returns:
    -------
    pd.DataFrame
        A DataFrame containing the forecast results, including predicted values and confidence intervals.
    """
    model = Prophet(seasonality_mode='multiplicative')
    model.fit(data)

    future = model.make_future_dataframe(periods=periods, freq='MS')

    forecast = model.predict(future)

    return forecast
