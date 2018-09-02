from trading.kraken import table_mapping, ohlc_table
from trading.sql import connect, meta, window_query, execute, time_range
from trading.strategy.simple import create
from trading.core import TradeCommand
from os.path import join as join_path

def simple_strategy():

    db = connect("sqlite:///" + join_path('/home/kristian/projects/trading/data',
                                          'ohlc-2018-08-19-23:32:55.sqlite'))

    ohlc = {**db,
            **table_mapping[ohlc_table],
            **{"table_object": meta(**db).tables[ohlc_table]}}

    offset = 3600
    window_size = 3600 * 5
    start, end = time_range(**ohlc)
    begin = start + offset

    query = window_query(**{**{"start": begin,
                               "end": begin + window_size},
                            **ohlc})

    data = execute(query=query, connection=db['connection'])

    return create(lambda: 0,
                  {TradeCommand.buy: lambda analysis: print("BUY!!"),
                   TradeCommand.sell: lambda analysis: print("SELL!!")}) + \
                   (data, ohlc)
