from typing import Any, Awaitable, Callable
from nats.aio.client import Client as NATS
from nats.aio.msg import Msg

from app.settings import settings


class NATSClient():
    def __init__(self):
        self._client = NATS()

    async def connect(self):
        await self._client.connect(servers=[settings.NATS_URL])

    async def subscribe(self, subject: str, callback: Callable[[Msg], Awaitable[None]]):
        await self._client.subscribe(subject, cb=callback)  # type: ignore

    async def publish(self, subject: str, payload: bytes):
        await self._client.publish(subject, payload)

    async def close(self):
        await self._client.drain()


class NATSEventBus():
    def __init__(self, client: NATSClient):
        self._nats_client = client

    async def start(
        self,
        listen_subject: str,
        publish_subject: str,
        callback: Callable[[], Awaitable[Any]],
        formatter: Callable[[Any], bytes]
    ) -> None:
        """
        Handles communication with NATS by connecting, subscribing to an event, and publishing a response.

        Attributes:
            _nats_client (NATSClient): An instance of the NATS client used for communication.
        """
        await self._nats_client.connect()

        async def wrapper(msg: Msg) -> None:
            dataclass_obj = await callback()
            payload = formatter(dataclass_obj)

            await self._nats_client.publish(publish_subject, payload)

        await self._nats_client.subscribe(listen_subject, callback=wrapper)

    async def shutdown(self):
        await self._nats_client.close()
