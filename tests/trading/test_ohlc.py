import sqlite3
from trading.kraken import get_rate


# def get_rate():
#     api = krakenex.API()
#     k = KrakenAPI(api)
#     #ohlc, last = k.get_ohlc_data("BCHUSD")
#     #ohlc, last = k.get_ohlc_data("XXMRZEUR")
#     return k.get_ohlc_data("XXMRZEUR")


def memdb():
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    return con, cur


def sql():
    conn, cur = memdb()
    try:
        ohlc, last = get_rate()
    except Exception as e:
        print("Exception")
        print(e)
    ohlc.to_sql('ohlc', conn, index=False)
    cur.execute("SELECT * FROM sqlite_master WHERE type='table';")
    print(cur.fetchall())
