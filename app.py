from ohlc import readjsonfile
from datetime import datetime
from matplotlib.dates import epoch2num
import matplotlib.pyplot as plt
import numpy as np


#record[0] = datetime.datetime.fromtimestamp(record[0])
def plot():
    x = [x[0] for x in readjsonfile("/home/kristian/projects/kraken-bash/ohlc.json")]
    y = [y[1] for y in readjsonfile("/home/kristian/projects/kraken-bash/ohlc.json")]
    print y

    z = np.polyfit(x, y, 2)
    f = np.poly1d(z)

    x_new = np.linspace(x[0], x[-1], 50)
    y_new = f(x_new)

    plt.plot(x,y,'o', x_new, y_new)
    # xs = readjsonfile("/home/kristian/projects/kraken-bash/ohlc.json")[:,0]
    # ys = readjsonfile("/home/kristian/projects/kraken-bash/ohlc.json")[:,1]
    # plt.plot(epoch2num(x), y)
    # plt.plot(x, y)
    # plt.gcf().autofmt_xdate()
    plt.ylabel('Price in EURO')
    plt.show()

if __name__ == "__main__":
    plot()
