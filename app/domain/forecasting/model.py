import pandas as pd
from prophet import Prophet


def forecast(data: pd.DataFrame, periods: int = 6) -> pd.DataFrame:
    model = Prophet(seasonality_mode='multiplicative')
    model.fit(data)

    future = model.make_future_dataframe(periods=periods, freq='MS')

    forecast = model.predict(future)

    return forecast
