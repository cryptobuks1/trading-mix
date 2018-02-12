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
    print "ohlc_1513226220"
    print_start_end(ohlc_1513226220)

    ohlcdata = ohlc_1513226220
    ohlcdata_sub = [record for record in ohlcdata if record[0] < 1513245588]
    xidx=0
    yidx=1
    [x, y, x_new, y_new, peaks] = fit(extract(ohlcdata, xidx, yidx))
    [x_sub, y_sub, x_sub_new, y_sub_new, peaks_sub] = fit(extract(ohlcdata_sub, xidx, yidx))
    trade = np.array([t + 5 for t in peaks])
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
