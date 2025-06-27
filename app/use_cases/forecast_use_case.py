import logging
import uuid

from app.domain.entities.forecast import Forecast
from app.domain.forecasting.forecast_adapter import forecast_adapter
from app.domain.forecasting.model import forecast
from app.domain.forecasting.sales_adapter import sales_adapter
from app.domain.value_objects.sales_data import SalesData


def forecast_use_case(sales_data: SalesData) -> Forecast:
    trace_id = str(uuid.uuid4())

    adapted_sales_data = sales_adapter(sales_data)
    logging.info(f"[trace_id={trace_id}] Starts forecasting...")
    new_forecast = forecast(adapted_sales_data)
    logging.info(f"[trace_id={trace_id}] Forecasting completed.")
    return forecast_adapter(new_forecast)
