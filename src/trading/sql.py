import sqlite3
from sqlalchemy.sql import select


def window(cur, start, end, time_column='time', table='ohlc'):
    start = int(start)
    end = int(end)
    cur.execute("""SELECT {0}, open
    FROM {1}
    WHERE {0} >= ? AND {0} < ? """.format(time_column, table), (start, end))
    result = cur.fetchall()
    return result


def memdb():
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    return con, cur


def time_range(cur=None, time_column='time', table='ohlc', **kwargs):
    if 'connection' not in kwargs:
        cur.execute("SELECT min({}) FROM {}".format(time_column, table))
        start = int(cur.fetchall()[0][0])
        cur.execute("SELECT max({}) FROM {}".format(time_column, table))
        end = int(cur.fetchall()[0][0])
    else:
        start = 0
        end = 1
    return start, end


def latest(cur, time_column='time', table='ohlc'):
    start, end = time_range(cur, time_column, table)
    return cur.execute("SELECT {0}, open ")
