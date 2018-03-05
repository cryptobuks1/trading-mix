import matplotlib.pyplot as plt
import numpy as np
import peakutils

def fit(coord):
    x, y = coord
    z = np.polyfit(x, y, 2)
    f = np.poly1d(z)
    x_new = np.linspace(x[0], x[-1], 50)
    y_new = f(x_new)
    peaks = peakutils.indexes(y_new, thres=0.5, min_dist=30)
    return [x, y, x_new, y_new, peaks]

def extract(data, xidx=0, yidx=1):
    return [[record[xidx] for record in data],
            [record[yidx] for record in data]]


if __name__ == "__main__":
    from ohlc import readjsonfile
    ohlc_1513226220 = [record for record in readjsonfile("/home/kristian/projects/kraken-bash/ohlc-1513226220.json")]
    xidx = 0
    yidx = 1
    [x, y, x_fit, y_fit, peaks_fit] = fit(extract(ohlc_1513226220, xidx, yidx))
    plt.plot(x, y, x_fit, y_fit, x_fit[peaks_fit], y_fit[peaks_fit], '+')
    plt.show()
