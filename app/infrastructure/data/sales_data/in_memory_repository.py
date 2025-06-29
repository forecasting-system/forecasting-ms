import asyncio
from app.domain.value_objects.sales_data import SalesData, SalesEntry
from tests.mock_data.mock_sales_data import mock_sales_data


class InMemorySalesDataRepository():
    # Component for testing purposes

    async def get_sales_data(self) -> SalesData:
        await asyncio.sleep(0)
        entries = [SalesEntry(sales_entry[0], sales_entry[1])
                   for sales_entry in mock_sales_data]

        return SalesData(entries=entries)
