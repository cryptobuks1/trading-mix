from trading.kraken import get_rate, ohlc
from trading.sql import memdb, window, time_range

latest_data_cur = ohlc()
start, end = time_range(latest_data_cur)
data = window(latest_data_cur, end - 3600 * 3, end)
