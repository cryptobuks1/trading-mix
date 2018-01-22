from ohlc import readjsonfile
from matplotlib.dates import epoch2num
import matplotlib.pyplot as plt
import numpy as np
import peakutils
from util import print_start_end, toDate
from data import fit, extract

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
    xidx = 0
    yidx = 1
    [x, y] = xandy = extract(ohlcdata, xidx, yidx)
    [x_new, y_new, peaks] = fit(xandy)
    [x_sub_new, y_sub_new, peaks_sub] = fit(extract(ohlcdata, xidx, yidx))
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
    plots.extend([x_new, y_new])
    plots.extend([x_new[peaks], y_new[peaks], 'r+'])
    plots.extend([x_new[trade], y_new[trade], 'y+'])
    plots.extend([x_sub_new, y_sub_new])
    plots.extend([x_sub_new[peaks_sub], y_sub_new[peaks_sub], '+'])


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
