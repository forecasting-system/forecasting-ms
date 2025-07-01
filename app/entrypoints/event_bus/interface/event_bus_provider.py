from typing import Any, Awaitable, Callable, Protocol

from app.domain.entities.forecast import Forecast


class EventBus(Protocol):

    async def start(
            self,
            listen_subject: str,
            publish_subject: str,
            callback: Callable[[], Awaitable[Forecast]],
            formatter: Callable[[Any], bytes]):
        ...

    async def shutdown(self):
        ...
