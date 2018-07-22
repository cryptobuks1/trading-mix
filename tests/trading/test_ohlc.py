from trading.kraken import get_rate, to_sql
from trading.sql import memdb
import pytest


@pytest.mark.ohlc
def test_sql():
    try:
        ohlc, last = get_rate()
    except Exception as e:
        print("Exception")
        print(e)
    con = to_sql(ohlc, 'ohlc')
    q = "SELECT * FROM sqlite_master WHERE type='table';"
    dsl = con.execute(q).fetchall()[0][4]

    assert 'open' in dsl
    assert 'high' in dsl
    assert 'low' in dsl
    assert 'close' in dsl
