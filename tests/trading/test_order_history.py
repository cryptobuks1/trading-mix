from trading.kraken import get_orders
from trading.sql import time_range
from trading.data import load_data_from_file
from os.path import join
from os import getcwd
from trading.sql import connect, latest, meta
from trading.kraken import to_sql


def test_orders():
    orders_cur = get_orders()
    start, end = time_range(orders_cur, table='orders')
    print(start, end)


def load_orders():
    path = join(getcwd(), 'data', 'orders.sqlite')
    orders = load_data_from_file(path)
    db = connect('sqlite://')
    to_sql(orders, 'ohlc', **db)
    db['meta_data'] = meta(db['connection'])
    latest_order = latest(**db)
    print(latest_order.time)
