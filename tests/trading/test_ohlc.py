import sqlite3
from trading.kraken import get_rate


# def get_rate():
#     api = krakenex.API()
#     k = KrakenAPI(api)
#     #ohlc, last = k.get_ohlc_data("BCHUSD")
#     #ohlc, last = k.get_ohlc_data("XXMRZEUR")
#     return k.get_ohlc_data("XXMRZEUR")


def memdb():
    return sqlite3.connect(":memory:")


def sql():
    conn = memdb()
    ohlc, last = get_rate()
    ohlc.to_sql('ohlc', conn, index=False)
    print(type(ohlc))
