import matplotlib.pyplot as plt
import numpy as np
import peakutils

def fit(data, xidx, yidx):
    x = [record[xidx] for record in data]
    y = [record[yidx] for record in data]
    z = np.polyfit(x, y, 2)
    f = np.poly1d(z)
    x_new = np.linspace(x[0], x[-1], 50)
    y_new = f(x_new)
    peaks = peakutils.indexes(y_new, thres=0.5, min_dist=30)
    print peaks
    return [x_new, y_new, peaks]

if __name__ == "__main__":
    from ohlc import readjsonfile
    ohlc_1513226220 = [record for record in readjsonfile("/home/kristian/projects/kraken-bash/ohlc-1513226220.json")]
    xidx = 0
    yidx = 1
    [x, y, peaks] = fit(ohlc_1513226220, xidx, yidx)
    plt.plot(x, y, x[peaks], y[peaks], '+')
    plt.show()
