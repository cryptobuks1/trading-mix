import trading.kraken as kr
from trading.sql import time_range, connect


def test_get_orders():
    db = connect('sqlite://')
    orders_cur = kr.get_orders(**db)
    print(orders_cur)
    window_span = time_range(**db)
    print(window_span)
