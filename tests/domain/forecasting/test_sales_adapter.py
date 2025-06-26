import pandas as pd

from app.domain.forecasting.sales_adapter import sales_adapter
from app.domain.value_objects.sales_data import SalesData, SalesEntry
from tests.mock_data.mock_sales_data import mock_sales_data


def test_sales_adapter_output_format():
    first_date = mock_sales_data[0][0]
    entries = [SalesEntry(sales_entry[0], sales_entry[1])
               for sales_entry in mock_sales_data]

    sales_data = SalesData(entries=entries)
    df = sales_adapter(sales_data)

    # Check structure
    assert isinstance(df, pd.DataFrame)
    assert list(df.columns)[0] in ["y", "ds"]
    assert list(df.columns)[1] in ["y", "ds"]
    assert df.index.name == "ds"
    assert df.index.freqstr == "MS"

    # Check content
    expected_dates = pd.date_range(
        first_date, periods=len(mock_sales_data), freq="MS")
    expected_values = [entry[1] for entry in mock_sales_data]

    assert all(df.index == expected_dates)
    assert df["y"].tolist() == expected_values
    assert all(df["ds"] == expected_dates)
