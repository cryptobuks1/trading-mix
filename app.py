from trading.kraken import ohlc
from trading.sql import window, time_range
from trading.data import fit, extract
from trading.octave import peaks
import matplotlib.pyplot as plt


def main():
    fig, ax = plt.subplots()
    latest_data_cur = ohlc()
    start, end = time_range(latest_data_cur)
    data = window(latest_data_cur, end - 3600 * 3, end)
    xs, ys, x_new, y_new, f = fit(extract(data))
    ps = peaks(y_new)
    print(ps[1][0])
    ax.plot(x_new, y_new, x_new[ps[1][0]], y_new[ps[1][0]], "r+")
    plt.show()
