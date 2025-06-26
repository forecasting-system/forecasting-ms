import pandas as pd

from app.domain.value_objects.sales_data import SalesData


def sales_adapter(sales_data: SalesData) -> pd.DataFrame:
    dates = pd.to_datetime([entry.date for entry in sales_data.entries])
    values = [entry.value for entry in sales_data.entries]

    df = pd.DataFrame({
        "ds": dates,
        "y": values
    })

    df["ds"] = df["ds"].dt.to_period("M").dt.to_timestamp()
    df.index = df["ds"]
    df.index.freq = "MS"

    return df
