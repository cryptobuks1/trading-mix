from os import getenv
from trading.kraken import ohlc
from trading.sql import window, time_range
from trading.data import analyseData, DoNotKnowHowToTrade
from trading.misc import desctructDict
from trading.octave import conf as peakConf
from trading.control import handleError


def main():
    dataDir = getenv("TRADING_DATA_DIR")
    latest_data_cur = ohlc()
    start, end = time_range(latest_data_cur)
    data = window(latest_data_cur, end - 3600 * 3, end)
    try:
        result = analyseData(peakConf, data)
        print("Try")
    except DoNotKnowHowToTrade as e:
        handleError(e)
        print("Exception")
    else:
        xfit, yfit, xpeak, ypeak, trade = desctructDict(result,
                                                        ("xfit",
                                                         "yfit",
                                                         "xpeak",
                                                         "ypeak",
                                                         "tradeAdvise"))
        if xpeak:
        print(trade)
