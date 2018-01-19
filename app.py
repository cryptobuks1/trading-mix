from ohlc import readjsonfile
from matplotlib.dates import epoch2num
import matplotlib.pyplot as plt
import numpy as np
import peakutils
from util import print_start_end, toDate

def plot():
    #datafile = "/home/kristian/projects/kraken-bash/ohlc-1513269300.json"
    datafile = "/home/kristian/projects/kraken-bash/ohlc-1516320660.json"
    ohlc_1513226220 = [record for record in readjsonfile("/home/kristian/projects/kraken-bash/ohlc-1513226220.json")]
    ohlc_1513269300 = [record for record in readjsonfile("/home/kristian/projects/kraken-bash/ohlc-1513269300.json")]
    ohlc_1516217100 = [record for record in readjsonfile("/home/kristian/projects/kraken-bash/ohlc-1516217100.json")]
    ohlc_1516320660 = [record for record in readjsonfile("/home/kristian/projects/kraken-bash/ohlc-1516320660.json")]
    print_start_end(ohlc_1513226220)

    ohlcdata = ohlc_1513226220
    x = [record[0] for record in ohlcdata]
    y = [record[1] for record in ohlcdata]
    x40 = x[0:360]
    y40 = y[0:360]
    data40 = [x40, y40]

    z = np.polyfit(x, y, 2)
    f = np.poly1d(z)


    x_new = np.linspace(x[0], x[-1], 50)
    y_new = f(x_new)
    peaks = peakutils.indexes(y_new, thres=0.5, min_dist=30)
    # print datetime.fromtimestamp(x[0])
    print x_new[peaks[0]]
    print toDate(x_new[peaks[0]])
    # trade = np.array([yt + 10 for yt in peaks])
    plots = [x,y,'o']
    plots.extend(data40)
    plots.extend([x_new, y_new])
    plots.extend([x_new[peaks], y_new[peaks], '+'])

    # plt.plot(
    #          x_new, y_new,
    #          x_new[peaks],y_new[peaks],'+',
    #          x_new[trade], y_new[trade],'+'
    # )
    plt.plot(* plots)
    plt.ylabel('Price in EURO')
    plt.show()

if __name__ == "__main__":
    plot()
