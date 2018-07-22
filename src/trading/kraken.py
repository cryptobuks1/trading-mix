import krakenex
from pykrakenapi import KrakenAPI
from trading.sql import memdb


def credentials(separator = '='):
    result_dict = {}
    with open('/home/kristian/.kraken') as f:
        for line in f:
            parts = line.split(separator, 1)
            result_dict[parts[0]] = parts[1].rstrip()
    return result_dict


creds_dict = credentials()
api = krakenex.API(creds_dict['APIKEY'],
                   creds_dict['PRIVATEKEY'])
k = KrakenAPI(api)


def get_rate():
    return k.get_ohlc_data("XXMRZEUR")


def to_sql(panda, table_name, **kwargs):
    env = kwargs.copy()
    if 'connection' not in env:
        env.update(memdb())
    con = env['connection']
    panda.to_sql(table_name, con, index=False)
    return con


def get_orders(**kwargs):
    orders, matches_cnt = k.get_trades_history()
    return to_sql(orders, 'orders', **kwargs)


def ohlc():
    try:
        ohlc, last = get_rate()
    except Exception as e:
        print("Exception")
        print(e)
    return to_sql(ohlc, 'ohlc')


orders_table = "ohlc"
table_mapping = {orders_table: {"table": orders_table,
                                "time_column": "timestamp"}}
