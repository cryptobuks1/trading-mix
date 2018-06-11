from trading.kraken import get_orders
from trading.sql import time_range


def test_orders():
    orders_cur = get_orders()
    start, end = time_range(orders_cur, table='orders')
    print(start, end)
