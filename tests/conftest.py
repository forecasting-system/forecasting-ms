import pytest
from fastapi.testclient import TestClient

from app.entrypoints.main import app

MOCK_DATA_PATH = "tests/mock_data/mock_data.csv"
SALES_COLUMN = "Sales_quantity"


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)
