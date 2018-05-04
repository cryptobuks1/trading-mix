def window(con, start, end):
    cur = con.cursor()
    cur.execute("SELECT timestamp, open FROM ohlc WHERE timestamp >= ? AND timestamp < ? ", (start, end))
    result = cur.fetchall()
    return result
