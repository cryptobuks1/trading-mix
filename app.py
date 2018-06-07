from trading.kraken import ohlc
from trading.sql import window, time_range
from trading.data import analyseData
from trading.misc import desctructDict
from trading.octave import conf as peakConf


def main():
    latest_data_cur = ohlc()
    start, end = time_range(latest_data_cur)
    data = window(latest_data_cur, end - 3600 * 3, end)
    result = analyseData(peakConf, data)
    xfit, yfit, xpeak, ypeak, trade = desctructDict(result, ("xfit",
                                                             "yfit",
                                                             "xpeak",
                                                             "ypeak",
                                                             "tradeAdvise"))
    print(trade)
