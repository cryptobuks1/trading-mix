from trading.kraken import ohlc
from trading.sql import window, time_range
from trading.data import analyseData
from trading.misc import desctructDict
from trading.octave import peaks
import matplotlib.pyplot as plt


def main():
    fig, ax = plt.subplots()
    latest_data_cur = ohlc()
    start, end = time_range(latest_data_cur)
    data = window(latest_data_cur, end - 3600 * 3, end)
    result = analyseData(data, {"fn": peaks,
                                "valuePos": 0,
                                "indexPos": 1})
    xfit, yfit, xpeak, ypeak = desctructDict(result, ("xfit",
                                                      "yfit",
                                                      "xpeak",
                                                      "ypeak"))
    ax.plot(xfit, yfit, xpeak, ypeak, 'r+')
    plt.show()
