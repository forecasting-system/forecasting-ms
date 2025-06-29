from typing import Protocol

from app.domain.value_objects.sales_data import SalesData


class SalesDataRepository(Protocol):
    async def get_sales_data(self) -> SalesData: ...
