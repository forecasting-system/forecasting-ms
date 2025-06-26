import pandas as pd

from app.domain.entities.forecast import Forecast, ForecastPoint


def forecast_adapter(forecast: pd.DataFrame) -> Forecast:
    if 'ds' not in forecast.columns or 'yhat' not in forecast.columns:
        raise ValueError(
            "Forecast DataFrame must contain 'ds' and 'yhat' columns.")

    # Drop rows with missing values in the required columns
    forecast_cleaned = forecast.dropna(subset=['ds', 'yhat'])

    points = []
    for _, row in forecast_cleaned.iterrows():
        point = ForecastPoint(date=row['ds'].date(), y=row['yhat'])
        points.append(point)

    return Forecast(points=points)
