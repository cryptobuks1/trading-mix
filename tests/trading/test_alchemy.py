# from sqlalchemy.sql import select
import trading.kraken as kr
import sqlite3


def test_get_orders():
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    orders_cur = kr.get_orders(connection=con,
                               cursor=cur)
    orders_cur.execute('SELECT * FROM orders')
