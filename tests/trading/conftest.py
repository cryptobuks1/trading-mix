import pytest
from os import getcwd
from os.path import join
from trading.data import load_data_from_file
from trading.sql import connect, meta, latest
from trading.kraken import to_sql


@pytest.fixture
def low_peak():
    path = join(getcwd(), 'data', 'low_pickle.byte')
    return load_data_from_file(path)


@pytest.fixture
def high_peak():
    path = join(getcwd(), 'data', 'high_pickle.byte')
    return load_data_from_file(path)


@pytest.fixture
def latest_order():
    path = join(getcwd(), 'data', 'orders.sqlite')
    orders = load_data_from_file(path)
    db = connect('sqlite://')
    to_sql(orders, 'ohlc', **db)
    db['meta_data'] = meta(db['connection'])
    return latest(**db)


@pytest.fixture
def high_peak_order_epoc(high_peak):
    return high_peak['result']['xpeak'][0]
