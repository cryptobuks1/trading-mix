from ohlc import readjsonfile
from datetime import datetime
from matplotlib.dates import epoch2num
import matplotlib.pyplot as plt
import numpy as np
import peakutils


def plot():
    datafile = "/home/kristian/projects/kraken-bash/ohlc-1513269300.json"
    datafile = "/home/kristian/projects/kraken-bash/ohlc.json"
    ohlcdata = [record for record in readjsonfile(datafile)]
    x = [record[0] for record in ohlcdata]
    y = [record[1] for record in ohlcdata]

    z = np.polyfit(x, y, 2)
    f = np.poly1d(z)


    x_new = np.linspace(x[0], x[-1], 50)
    y_new = f(x_new)
    peaks = peakutils.indexes(y_new, thres=0.5, min_dist=30)
    print datetime.fromtimestamp(x[0])
    print datetime.fromtimestamp(x[peaks[0]])
    trade = np.array([yt + 10 for yt in peaks])

    plt.plot(x,y,'o',
             x_new, y_new,
             x_new[peaks],y_new[peaks],'+',
             x_new[trade], y_new[trade],'+'
    )
    plt.ylabel('Price in EURO')
    plt.show()

if __name__ == "__main__":
    plot()
