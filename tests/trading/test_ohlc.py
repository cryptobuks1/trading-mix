from trading.kraken import get_rate
from trading.sql import memdb, window


def sql():
    conn, cur = memdb()
    try:
        ohlc, last = get_rate()
    except Exception as e:
        print("Exception")
        print(e)
    ohlc.to_sql('ohlc', conn, index=False)
    window(conn)
    cur.execute("SELECT * FROM sqlite_master WHERE type='table';")
    print(cur.fetchall())
