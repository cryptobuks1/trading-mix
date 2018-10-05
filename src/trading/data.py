import matplotlib.pyplot as plt
import numpy as np
from blinker import signal
from enum import Enum
from trading.sql import window, time_range
from trading.octave import conf as peakConf
from trading.util import toDate
import pickle
import logging
from time import sleep


class TradeCommand(Enum):
    sell = 1
    buy = 2
    wait = 3


def fit(coord, **kwargs):
    order = kwargs.get('fit_order', 2)
    full = kwargs.get("fit_full", True)
    cov = kwargs.get("fit_cov", False)
    x, y = coord
    z = np.polyfit(x, y, order, full=full, cov=cov)
    # print("Fit")
    # print(z)
    if full or cov:
        f = np.poly1d(z[0])
    else:
        f = np.poly1d(z)
    x_new = np.linspace(x[0], x[-1], 50)
    y_new = f(x_new)
    return [x, y, x_new, y_new, f, z]


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


def analyseData(peakConf, data, **kwargs):
    logging.debug("Start analysis")
    x, y, xfit, yfit, ff, z = fit(extract(data), **kwargs)
    peakFn, indexPos = [peakConf[k] for k in ('fn', 'indexPos')]
    peaks = peakFn(yfit, **kwargs)
    peaksIndex = peaks[indexPos]
    result = {'x': x,
              'y': y,
              'xfit': xfit,
              'yfit': yfit,
              'xpeak': xfit[peaksIndex],
              'ypeak': yfit[peaksIndex],
              'z': z}
    if result['xpeak']:
        try:
            event = kwargs['foundPeakEvent']
        except Exception:
            event = signal('foundPeak')
    else:
        try:
            event = kwargs['noPeakEvent']
        except Exception:
            event = signal('noPeak')

    event.send('analyse', data={'data': data, 'result': result})
    return result


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
        result = window(env['connection'], **env)
        logging.debug("Found Result")
        if result:
            yield result


def pause_frame_generator(state, generator):
    for frame in generator:
        if state['continue']:
            yield frame
        else:
            while not state['continue']:
                sleep(0.3)


def next_peak(**kwargs):
    for data in window_generator(3600 * 3, 600, **kwargs):
        result = analyseData(peakConf, data)
        if result["xpeak"]:
            yield result


def is_new_peak(latest_order_epoc, analysis, **kwargs):
    '''
    TODO: rename to good peak
    '''
    loe = latest_order_epoc()
    peakEpoc = analysis['xpeak'][0]
    logging.debug("Peak at: {}".format(toDate(peakEpoc)))
    logging.debug("Peak price: {}".format(analysis['ypeak'][0]))
    logging.debug("Latest order epoc: {}".format(toDate(loe)))
    logging.debug("First fit prize: {}".format(analysis['yfit'][0]))
    logging.debug("Last fit prize: {}".format(analysis['yfit'][-1]))
    timeDiff = abs(peakEpoc - loe)
    logging.debug("Diff between latest order and current peak: {}".format(toDate(timeDiff)))

    # Price distance from peak
    logging.debug("Price distance {}".format(abs(analysis['ypeak'][0] - analysis['yfit'][0])))
    # if advice(analysis) == TradeCommand.buy:

    if abs(analysis['ypeak'][0] - analysis['yfit'][0]) > 1:
        logging.debug("Distance too big")
        return False
    # valley J bad
    # if analysis['yfit'][0] > analysis['yfit'][-1]:
    #     return True
    minimum_peak_distance = kwargs.get('minimum_peak_distance',
                                       3600 * 1.5)  # default 1.5 hour
    return peakEpoc > loe and timeDiff > minimum_peak_distance


def advice(analysis):
    z = analysis['z']
    if z[0][1] < 0:
        return TradeCommand.buy
    else:
        return TradeCommand.sell


def load_data_from_file(path):
        with open(path, 'rb') as f:
            lp = pickle.load(f)
            return lp


if __name__ == "__main__":
    from ohlc import readjsonfile
    ohlc_1513226220 = [record for record in readjsonfile("/home/kristian/projects/kraken-bash/ohlc-1513226220.json")]
    xidx = 0
    yidx = 1
    [x, y, x_fit, y_fit, peaks_fit] = fit(extract(ohlc_1513226220, xidx, yidx))
    plt.plot(x, y, x_fit, y_fit, x_fit[peaks_fit], y_fit[peaks_fit], '+')
    plt.show()
