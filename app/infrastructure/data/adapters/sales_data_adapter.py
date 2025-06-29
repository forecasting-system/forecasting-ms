from datetime import date
from app.domain.value_objects.sales_data import SalesData, SalesEntry


def sales_data_adapter(sales_data: dict[str, list[dict[str, str | int]]]) -> SalesData:
    entries = [SalesEntry(date.fromisoformat(sales_entry["date"]), sales_entry["value"])
               for sales_entry in sales_data["entries"]]
    return SalesData(entries=entries)
