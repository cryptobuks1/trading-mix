from os.path import join
from trading.sql import connect, time_range
from trading.kraken import table_mapping, orders_table


def test_yield_peak():
    print(join('/home/kristian/projects/trading/data',
               'alldata.sqlite'))
    db = connect("sqlite:///" + join('/home/kristian/projects/trading/data',
                                     'alldata.sqlite'))
    env = {**db, **table_mapping[orders_table]}
    start, end = time_range(**env)
    print(start, end)
