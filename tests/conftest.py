import pytest
from fastapi.testclient import TestClient

from app.entrypoints.main import app
from app.settings import settings

MOCK_DATA_PATH = "tests/mock_data/mock_data.csv"
SALES_COLUMN = "Sales_quantity"


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def override_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(settings, "USE_MOCK_DATA", False)
