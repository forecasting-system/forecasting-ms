import pandas as pd
import pytest
from fastapi.testclient import TestClient

from app.api.main import app

MOCK_DATA_PATH = "tests/mock_data/mock_data.csv"
SALES_COLUMN = "Sales_quantity"


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def a_valid_dataset() -> pd.DataFrame:
    df = pd.read_csv(MOCK_DATA_PATH, index_col="Period",
                     dayfirst=True, parse_dates=True)
    df.index.freq = 'MS'

    df: pd.DataFrame = df[[SALES_COLUMN]].copy()
    df = df.rename(columns={SALES_COLUMN: "y"})
    df["ds"] = df.index
    df["ds"] = df["ds"].dt.to_period("M").dt.to_timestamp()

    return df
