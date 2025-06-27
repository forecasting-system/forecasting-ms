from app.domain.value_objects.sales_data import SalesData, SalesEntry
from app.domain.entities.forecast import Forecast
from app.use_cases.forecast_use_case import forecast_use_case
from tests.mock_data.mock_sales_data import mock_sales_data


def test_forecast_use_case_returns_forecast():

    entries = [SalesEntry(sales_entry[0], sales_entry[1])
               for sales_entry in mock_sales_data]

    sales_data = SalesData(entries=entries)

    result = forecast_use_case(sales_data)

    assert isinstance(result, Forecast)
    # If Forecast has fields, check them
    assert result.points is not None
    assert len(result.points) > 0
