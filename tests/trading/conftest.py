
import pytest
from os import getcwd
from os.path import join, dirname
from sys import path
from trading.data import load_data_from_file
from trading.sql import connect, meta, latest
from trading.kraken import to_sql

try:
    path.append(join(dirname(__file__), 'helpers'))
except NameError:
    pass

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
    return high_peak['result']['xpeak'][0] + 1800


@pytest.fixture
def low_peak_order_epoc(low_peak):
    return low_peak['result']['xpeak'][0] + 1800

@pytest.fixture
def all_data():
    db = connect("sqlite:///" + join('/home/kristian/projects/trading/data',
                                       'ohlc-2018-08-19-23:32:55.sqlite'))
    # db['time_column'] = 'timestamp'
    return db


@pytest.fixture
def ohlc_12_hour_as_sql():
    db = connect("sqlite:///" + join('/home/kristian/projects/trading/data',
                                       'ohlc-2018-08-19-23:32:55.sqlite'))
    # db['time_column'] = 'timestamp'
    return db
