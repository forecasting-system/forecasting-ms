import uuid

from app.domain.entities.forecast import Forecast
from app.domain.forecasting.forecast_adapter import forecast_adapter
from app.domain.forecasting.model import forecast
from app.domain.forecasting.sales_adapter import sales_adapter
from app.use_cases.interfaces.sales_data_provider import SalesDataRepository
from app.use_cases.interfaces.logger import Logger


class ForecastUseCase:
    def __init__(self, sales_data_provider: SalesDataRepository, logger: Logger):
        self._sales_data_provider = sales_data_provider
        self._logger = logger

    async def execute(self) -> Forecast:
        trace_id = str(uuid.uuid4())

        sales_data = await self._sales_data_provider.get_sales_data()
        adapted_sales_data = sales_adapter(sales_data)

        self._logger.info(f"[trace_id={trace_id}] Starts forecasting...")
        new_forecast = forecast(adapted_sales_data)
        self._logger.info(f"[trace_id={trace_id}] Forecasting completed.")

        return forecast_adapter(new_forecast)
