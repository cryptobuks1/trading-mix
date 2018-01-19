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
    ohlcdata_sub = [record for record in ohlcdata if record[0] < 1513249991]
    x = [record[0] for record in ohlcdata]
    y = [record[1] for record in ohlcdata]
    x_sub = [record[0] for record in ohlcdata_sub]
    y_sub = [record[1] for record in ohlcdata_sub]
    x40 = x[0:360]
    y40 = y[0:360]
    data40 = [x40, y40]

    z = np.polyfit(x, y, 2)
    f = np.poly1d(z)
    z_sub = np.polyfit(x_sub, y_sub, 2)
    f_sub = np.poly1d(z_sub)


    x_new = np.linspace(x[0], x[-1], 50)
    y_new = f(x_new)
    x_sub_new = np.linspace(x_sub[0], x_sub[-1], 50)
    y_sub_new = f_sub(x_sub_new)



    peaks = peakutils.indexes(y_new, thres=0.5, min_dist=30)
    peaks_sub = peakutils.indexes(y_sub_new, thres=0.5, min_dist=30)
    # print datetime.fromtimestamp(x[0])
    print peaks
    print "peak"
    print int(x_new[peaks[0]])
    print toDate(x_new[peaks[0]])
    trade = np.array([t + 10 for t in peaks])
    print "trade"
    print int(x_new[trade[0]])
    print toDate(int(x_new[trade[0]]))
    plots = [x,y,'o']
    plots.extend(data40)
    plots.extend([x_new, y_new])
    plots.extend([x_sub_new, y_sub_new])
    plots.extend([x_new[peaks], y_new[peaks], 'r+'])
    plots.extend([x_sub_new[peaks_sub], y_sub_new[peaks_sub], '+'])
    plots.extend([x_new[trade], y_new[trade], 'y+'])

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
