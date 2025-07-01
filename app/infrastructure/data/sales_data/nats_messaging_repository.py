import asyncio
import json
import uuid

from nats.aio.client import Client as NATS
from nats.aio.errors import ErrTimeout
from nats.aio.msg import Msg
from app.domain.value_objects.sales_data import SalesData  # , SalesEntry
from app.infrastructure.data.adapters.sales_data_adapter import sales_data_adapter
from app.settings import settings
from app.constants import messages
from nats.errors import NoServersError


class NATSClient:
    def __init__(self):
        self._client = NATS()

    async def request(self, subject: str, payload: bytes, timeout: int = 2, max_reconnect_attempts: int = 2) -> bytes:
        await self._client.connect(servers=[settings.NATS_URL], connect_timeout=timeout)

        try:
            inbox = self._client.new_inbox()
            future = asyncio.Future()  # type: ignore

            async def response_handler(msg: Msg) -> None:
                if not future.done():
                    future.set_result(msg)  # type: ignore

            # Subscribe to the inbox
            await self._client.subscribe(  # type: ignore
                inbox,
                cb=response_handler
            )

            # Wrap message as NestJS expects
            correlation_id = str(uuid.uuid4())
            nest_payload = {
                "id": correlation_id,
                "pattern": subject,
                "data": json.loads(payload.decode())  # turn b'{}' into {}
            }

            await self._client.publish(subject, json.dumps(nest_payload).encode(), reply=inbox)

            try:
                msg = await asyncio.wait_for(future, timeout)  # type: ignore
                return msg.data  # type: ignore
            except asyncio.TimeoutError:
                raise RuntimeError("Timeout waiting for NATS response")

        finally:
            await self._client.close()


class NATSMessagingSalesDataRepository:
    def __init__(self, nats_client: NATSClient, subject: str = messages.SALES_GET_DATA):
        self._nats_client = nats_client
        self._subject = subject

    async def get_sales_data(self) -> SalesData:
        try:
            data = await self._nats_client.request(self._subject, b'{}')
            sales_data = json.loads(data)
            adapted_sales_data = sales_data_adapter(sales_data['response'])
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
