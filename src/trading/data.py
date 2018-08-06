import matplotlib.pyplot as plt
import numpy as np
import peakutils
from blinker import signal
from enum import Enum
from collections import namedtuple
from trading.sql import window, time_range
from trading.octave import conf as peakConf
from trading.control import handleError
import pickle
import logging


def fit(coord):
    x, y = coord
    z = np.polyfit(x, y, 2, full=True)
    # print("Fit")
    # print(z)
    f = np.poly1d(z[0])
    x_new = np.linspace(x[0], x[-1], 50)
    y_new = f(x_new)
    return [x, y, x_new, y_new, f, z]


class TradeCommand(Enum):
    sell = 1
    buy = 2
    wait = 3


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
    x, y, xfit, yfit, ff, z = fit(extract(data))
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
                yield frame


def next_peak(**kwargs):
    for data in window_generator(3600 * 3, 600, **kwargs):
        result = analyseData(peakConf, data)
        if result["xpeak"]:
            yield result



def is_new_peak(latest_order_epoc, analysis):
    peakEpoc = analysis['xpeak'][0]
    logging.debug("Peak at: %s", str(peakEpoc))
    logging.debug("Latest order epoc: %s", latest_order_epoc)
    timeDiff = abs(peakEpoc - latest_order_epoc)
    logging.debug("Diff between latest order and current peak: %s", timeDiff)
    return timeDiff > 1200  # within 20 minutes


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
