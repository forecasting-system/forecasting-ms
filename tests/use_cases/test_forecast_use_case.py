import pytest
from app.domain.entities.forecast import Forecast
from app.infrastructure.data.sales_data.in_memory_repository import InMemorySalesDataRepository
from app.infrastructure.logs.uvicorn_logger import UvicornLogger
from app.use_cases.forecast_use_case import ForecastUseCase


@pytest.mark.asyncio
async def test_forecast_use_case_returns_forecast():
    sales_data_provider = InMemorySalesDataRepository()
    forecast_use_case = ForecastUseCase(
        sales_data_provider=sales_data_provider, logger=UvicornLogger())

    result = await forecast_use_case.execute()

    assert isinstance(result, Forecast)
    assert result.points is not None
    assert len(result.points) > 0
