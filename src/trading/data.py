import matplotlib.pyplot as plt
import numpy as np
import peakutils
from enum import Enum
from trading.sql import window, time_range
from trading.octave import conf as peakConf
from trading.control import handleError


def fit(coord):
    x, y = coord
    z = np.polyfit(x, y, 2, full=True)
    f = np.poly1d(z[0])
    x_new = np.linspace(x[0], x[-1], 50)
    y_new = f(x_new)
    return [x, y, x_new, y_new, f]


def peaks(values):
    return peakutils.indexes(values, thres=0.5, min_dist=30)


def streamWindow(windowSize, step, data):
    '''
    windowSize: int, in seconds
    step: int, in seconds
    data: Sequence of ohlc data
    '''
    windows = []
    start = data[0][0] - step
    while True:
        start += step
        end = start + windowSize
        windowData = [dp
                      for dp in data
                      if start <= dp[0] < end]
        if windowData:
            windows.append(windowData)
        else:
            return windows


def extract(env, xidx=0, yidx=1):
    return [[int(record[xidx]) for record in env],
            [float(record[yidx]) for record in env]]


def analyseData(peakConf, data):
    x, y, xfit, yfit, ff = fit(extract(data))
    peakFn, indexPos = [peakConf[k] for k in ('fn', 'indexPos')]
    peaks = peakFn(yfit)
    peaksIndex = peaks[indexPos]
    return {'x': x,
            'y': y,
            'xfit': xfit,
            'yfit': yfit,
            'xpeak': xfit[peaksIndex],
            'ypeak': yfit[peaksIndex],
            'tradeAdvise': how_to_trade(peaksIndex, yfit)}


class TradeCommand(Enum):
    sell = 1
    buy = 2
    wait = 3


class DoNotKnowHowToTrade(Exception):
    pass


def how_to_trade(peak_list, ys):
    if not peak_list:
        return TradeCommand.wait
    peak = peak_list[0]
    before = peak - 1
    after = peak + 1
    if (before >= 0 and ys[before] < ys[peak]) or \
       (after < len(ys) and ys[after] < ys[peak]):
        return TradeCommand.sell
    elif (before >= 0 and ys[before] > ys[peak]) or \
         (after < len(ys) and ys[after] > ys[peak]):
        return TradeCommand.buy
    raise DoNotKnowHowToTrade


def fitChunks(data):
    """
    Parameters
    ----------
    data : list
           list of lists of ohlc data
    """
    map(lambda dl: fit(extract(dl)), data)


def window_generator(window_size, step_size, **kwargs):
    start, end = time_range(**kwargs)
    pos = 0
    while start + pos < end:
        step_start = start + pos
        span = {"start": step_start,
                "end": step_start + window_size}
        env = {**kwargs, **span}
        pos += step_size
        result = window(**env)
        if result:
            yield result


def pause_frame_generator(state, generator):
    for frame in generator:
        if state['continue']:
            print("Continue")
            yield frame
        else:
            while not state['continue']:
                yield frame


def next_peak(**kwargs):
    for data in window_generator(3600 * 3, 600, **kwargs):
        try:
            result = analyseData(peakConf, data)
        except DoNotKnowHowToTrade as e:
            handleError(e)
        else:
            if result["xpeak"]:
                yield result


if __name__ == "__main__":
    from ohlc import readjsonfile
    ohlc_1513226220 = [record for record in readjsonfile("/home/kristian/projects/kraken-bash/ohlc-1513226220.json")]
    xidx = 0
    yidx = 1
    [x, y, x_fit, y_fit, peaks_fit] = fit(extract(ohlc_1513226220, xidx, yidx))
    plt.plot(x, y, x_fit, y_fit, x_fit[peaks_fit], y_fit[peaks_fit], '+')
    plt.show()
