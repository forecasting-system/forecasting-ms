import json

from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout
from app.domain.value_objects.sales_data import SalesData, SalesEntry
from app.infrastructure.data.adapters.sales_data_adapter import sales_data_adapter
from app.settings import settings
from tests.mock_data.mock_sales_data import mock_sales_data
from app.constants import messages
from nats.errors import NoServersError


class NATSClient:
    def __init__(self):
        self._client = NATS()

    async def request(self, subject: str, payload: bytes, timeout: int = 2, max_reconnect_attempts: int = 2) -> bytes:
        await self._client.connect(
            servers=[settings.NATS_URL],
            connect_timeout=timeout,
            max_reconnect_attempts=max_reconnect_attempts)
        try:
            response = await self._client.request(subject, payload, timeout=timeout)
            return response.data
        finally:
            await self._client.close()


class NATSMessagingSalesDataRepository:
    def __init__(self, nats_client: NATSClient, subject: str = messages.SALES_GET_DATA):
        self._nats_client = nats_client
        self._subject = subject

    async def get_sales_data(self) -> SalesData:
        try:
            data = await self._nats_client.request(self._subject, b'')
            sales_data = json.loads(data)
            adapted_sales_data = sales_data_adapter(sales_data)
            return adapted_sales_data

        except ErrTimeout:
            raise RuntimeError("Timeout: no response from sales service")

        except NoServersError:
            raise RuntimeError("No messaging servers available")

        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in sales service response")

        except TypeError as e:
            raise ValueError(f"Malformed data for SalesData: {e}")

        except Exception as e:
            raise ValueError(f"Error getting sales data: {e}")

        finally:

            # TODO: remove this TEMP code
            if settings.USE_MOCK_DATA:
                entries = [SalesEntry(sales_entry[0], sales_entry[1])
                           for sales_entry in mock_sales_data]

                return SalesData(entries=entries)
