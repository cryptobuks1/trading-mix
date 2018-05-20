def window(con, start, end):
    start = int(start)
    end = int(end)
    cur = con.cursor()
    cur.execute("SELECT timestamp, open FROM ohlc WHERE timestamp >= ? AND timestamp < ? ", (start, end))
    result = cur.fetchall()
    return result
