from trading.kraken import get_rate
from trading.sql import memdb
import pytest


@pytest.mark.ohlc
def test_sql():
    db = memdb()
    con = db['connection']
    try:
        ohlc, last = get_rate()
    except Exception as e:
        print("Exception")
        print(e)
    ohlc.to_sql('ohlc', db['connection'], index=False)
    q = "SELECT * FROM sqlite_master WHERE type='table';"
    dsl = con.execute(q).fetchall()[0][4]

    assert 'open' in dsl
