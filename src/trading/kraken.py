import krakenex
from pykrakenapi import KrakenAPI
from trading.sql import memdb


def get_rate():
    api = krakenex.API()
    k = KrakenAPI(api)
    return k.get_ohlc_data("XXMRZEUR")


def ohlc():
    conn, cur = memdb()
    try:
        ohlc, last = get_rate()
    except Exception as e:
        print("Exception")
        print(e)
    ohlc.to_sql('ohlc', conn, index=False)
    return cur
