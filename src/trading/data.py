import matplotlib.pyplot as plt
import numpy as np
import peakutils


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
    windowSize in seconds
    step in seconds
    data: Sequence of ohlc data
    '''
    windows = []
    start = data[0][0] - step
    stopIter = lambda : (_ for _ in ()).throw(StopIteration) #Hack to stop generator
    while True:
        start += step
        end = start + windowSize
        windowData = (stopIter() if dp[0] >= end else dp
                      for dp in data
                      if start <= dp[0]) #Collect where start <= dp[0] < end
        if windowData:
            windows.append(windowData)
        else:
            return windows

def extract(env, xidx=0, yidx=1):
    return env.copy().update({'xs': [record[xidx] for record in env['data']],
                              'ys': [record[yidx] for record in env['data']]})

def analyseData(dl):
    x, y, xfit, yfit, ff = fit(extract(window))

def fitChunks(data):
    """
    Parameters
    ----------
    data : list
           list of lists of ohlc data
    """
    map(lambda dl: fit(extract(dl)), data)

if __name__ == "__main__":
    from ohlc import readjsonfile
    ohlc_1513226220 = [record for record in readjsonfile("/home/kristian/projects/kraken-bash/ohlc-1513226220.json")]
    xidx = 0
    yidx = 1
    [x, y, x_fit, y_fit, peaks_fit] = fit(extract(ohlc_1513226220, xidx, yidx))
    plt.plot(x, y, x_fit, y_fit, x_fit[peaks_fit], y_fit[peaks_fit], '+')
    plt.show()
