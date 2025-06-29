import json
from nats.aio.errors import ErrTimeout
import pytest

from app.constants import messages
from app.domain.value_objects.sales_data import SalesData
from app.infrastructure.data.sales_data.nats_messaging_repository import NATSMessagingSalesDataRepository


class MockNATSClient:
    async def request(self, subject: str, payload: bytes, timeout: float = 2.0) -> bytes:
        if subject == messages.SALES_GET_DATA:
            return json.dumps({
                "entries": [
                    {"date": "2024-01-01", "value": 100},
                    {"date": "2024-01-02", "value": 200}
                ]
            }).encode("utf-8")
        raise ValueError("Unknown subject")


@pytest.mark.asyncio
async def test_get_sales_data_success():
    repo = NATSMessagingSalesDataRepository(
        nats_client=MockNATSClient())  # type: ignore
    result = await repo.get_sales_data()

    assert isinstance(result, SalesData)
    assert len(result.entries) == 2
    assert result.entries[0].date.isoformat() == "2024-01-01"
    assert result.entries[0].value == 100


class FailingNATSClient:
    async def request(self, subject: str, payload: bytes, timeout: float = 2.0) -> bytes:
        raise ErrTimeout()


@pytest.mark.asyncio
async def test_get_sales_data_timeout():
    repo = NATSMessagingSalesDataRepository(
        nats_client=FailingNATSClient())  # type: ignore

    with pytest.raises(RuntimeError) as exc:
        await repo.get_sales_data()

    assert "Timeout" in str(exc.value)


class BadJsonNATSClient:
    async def request(self, subject: str, payload: bytes, timeout: float = 2.0) -> bytes:
        return b'{invalid_json}'


@pytest.mark.asyncio
async def test_get_sales_data_invalid_json():
    repo = NATSMessagingSalesDataRepository(
        nats_client=BadJsonNATSClient())  # type: ignore

    with pytest.raises(ValueError) as exc:
        await repo.get_sales_data()

    assert "Invalid JSON format" in str(exc.value)
