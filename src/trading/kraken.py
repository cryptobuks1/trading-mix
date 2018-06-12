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
    if 'connection' not in kwargs and 'cursor' not in kwargs:
        conn, cur = memdb()
    else:
        conn = kwargs['connection']
        cur = kwargs['cursor']
    panda.to_sql(table_name, conn, index=False)
    return cur


def get_orders(**kwargs):
    orders, matches_cnt = k.get_trades_history()
    return to_sql(orders, 'orders', **kwargs)


def ohlc():
    try:
        ohlc, last = get_rate()
    except Exception as e:
        print("Exception")
        print(e)
    conn, cur = memdb()
    ohlc.to_sql('ohlc', conn, index=False)
    return cur
