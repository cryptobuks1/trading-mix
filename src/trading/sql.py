import sqlite3


def window(cur, start, end):
    start = int(start)
    end = int(end)
    cur.execute("SELECT timestamp, open FROM ohlc WHERE timestamp >= ? AND timestamp < ? ", (start, end))
    result = cur.fetchall()
    return result


def memdb():
    con = sqlite3.connect(":memory:")
    cur = con.cursor()
    return con, cur


def min_max(cur, time_column='time', table='ohlc'):
    cur.execute("SELECT min({}) FROM {}".format(time_column, table))
    start = int(cur.fetchall()[0][0])
    cur.execute("SELECT max({}) FROM {}".format(time_column, table))
    end = int(cur.fetchall()[0][0])
    return start, end
