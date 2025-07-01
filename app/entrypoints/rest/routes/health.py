from fastapi import APIRouter, HTTPException

from app.domain.entities.forecast import Forecast
from app.infrastructure.data.sales_data.sales_repository_factory import get_sales_repository
from app.infrastructure.logs.uvicorn_logger import UvicornLogger
from app.settings import settings
from app.use_cases.forecast_use_case import ForecastUseCase

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/health_forecasting")
async def read_root() -> dict[str, Forecast]:
    try:
        sales_data_provider = get_sales_repository(
            settings.MESSAGING_SERVER)

        forecast_use_case = ForecastUseCase(
            sales_data_provider=sales_data_provider, logger=UvicornLogger())

        forecast = await forecast_use_case.execute()
        return {"forecast": forecast}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
