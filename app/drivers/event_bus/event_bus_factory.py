

from app.drivers.event_bus.interface.event_bus_provider import EventBus
from app.drivers.event_bus.nats_event_bus_service import NATSClient, NATSEventBus
from app.settings import EventServerType


def get_event_bus(type: EventServerType = EventServerType.NATS) -> EventBus:
    if type == EventServerType.NATS:
        nats_client = NATSClient()
        nats_event_bus = NATSEventBus(nats_client)
        return nats_event_bus
