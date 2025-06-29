
from app.domain.entities.forecast import Forecast
from app.infrastructure.data.sales_data.sales_repository_factory import get_sales_repository
from app.infrastructure.logs.uvicorn_logger import UvicornLogger
from app.settings import settings
from app.use_cases.forecast_use_case import ForecastUseCase


async def trigger_forecast() -> Forecast:
    sales_data_provider = get_sales_repository(
        settings.MESSAGING_SERVER)

    forecast_use_case = ForecastUseCase(
        sales_data_provider=sales_data_provider, logger=UvicornLogger())

    forecast = await forecast_use_case.execute()

    return forecast
