
from app.infrastructure.data.sales_data.in_memory_repository import InMemorySalesDataRepository
from app.infrastructure.data.sales_data.nats_messaging_repository import NATSClient, NATSMessagingSalesDataRepository
from app.settings import MessagingServerType
from app.use_cases.forecast_use_case import SalesDataRepository


def get_sales_repository(type: MessagingServerType = MessagingServerType.NATS) -> SalesDataRepository:

    if type == MessagingServerType.NATS:
        nats_client = NATSClient()
        sales_data_provider = NATSMessagingSalesDataRepository(nats_client)
        return sales_data_provider

    if type == MessagingServerType.IN_MEMORY:
        return InMemorySalesDataRepository()
