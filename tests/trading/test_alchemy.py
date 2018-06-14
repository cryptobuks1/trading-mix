import trading.kraken as kr
from trading.sql import time_range
from sqlalchemy import MetaData, create_engine


def test_get_orders():
    # con = sqlite3.connect(":memory:")
    con = create_engine('sqlite://')
    # cur = con.cursor()
    orders_cur = kr.get_orders(connection=con,
                               cursor=con)
    print(orders_cur)
    window_span = time_range(connection=con)
    print(window_span)
