from os.path import join
from trading.data import next_peak
from trading.kraken import table_mapping, orders_table
from trading.sql import connect, meta


def test_next_peak():
    db = connect("sqlite:///" + join('/home/kristian/projects/trading/data',
                                     'alldata.sqlite'))
    meta_data = {"meta_data": meta(**db)}
    env = {**db, **table_mapping[orders_table], **meta_data}
    result = next_peak(**env)
    print(next(result))
