from trading.kraken import get_rate
from trading.sql import memdb


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
