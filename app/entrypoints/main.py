import uvicorn

from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.constants import events
from app.entrypoints.event_bus.event_bus_factory import get_event_bus
from app.entrypoints.rest.routes.health import router as health_router
from app.entrypoints.subpub.trigger_forecast import trigger_forecast
from app.settings import settings
from app.use_cases.mappers.forecast_mapper import dataclass_to_nats_payload


event_bus = get_event_bus(settings.EVENT_SERVER)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await event_bus.start(
        listen_subject=events.SALES_PERSISTED,
        publish_subject=events.FORECAST_GENERATED,
        callback=trigger_forecast,
        formatter=dataclass_to_nats_payload
    )
    yield
    # Shutdown
    await event_bus.shutdown()

app = FastAPI(lifespan=lifespan)


app.include_router(health_router, prefix="", tags=["Health"])


def run():
    uvicorn.run("app.drivers.main:app", reload=True)
