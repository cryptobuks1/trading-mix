from trading.kraken import ohlc
from trading.sql import window, time_range
from trading.data import analyseData
from trading.misc import desctructDict
from trading.octave import conf as peakConf
import matplotlib.pyplot as plt
import matplotlib.dates as mdate


def test_plot():
    fig, ax = plt.subplots()
    latest_data_cur = ohlc()
    start, end = time_range(latest_data_cur)
    data = window(latest_data_cur, end - 3600 * 3, end)
    result = analyseData(peakConf, data)
    xs, ys, xfit, yfit, xpeak, ypeak = desctructDict(result, ('x',
                                                              'y',
                                                              "xfit",
                                                              "yfit",
                                                              "xpeak",
                                                              "ypeak"))
    xs = mdate.epoch2num(xs)
    xfit = mdate.epoch2num(xfit)
    xpeak = mdate.epoch2num(xpeak)
    ax.plot_date(xs, ys)
    ax.plot_date(xfit, yfit)
    ax.plot_date(xpeak, ypeak)
    # Choose your xtick format string
    date_fmt = '%d-%m-%y %H:%M:%S'

    # Use a DateFormatter to set the data to the correct format.
    date_formatter = mdate.DateFormatter(date_fmt)
    ax.xaxis.set_major_formatter(date_formatter)

    # Sets the tick labels diagonal so they fit easier.
    fig.autofmt_xdate()
    plt.show()
