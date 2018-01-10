from ohlc import readjsonfile
from datetime import datetime
from matplotlib.dates import epoch2num
import matplotlib.pyplot as plt
import numpy as np

def plot():
    x = [x[0] for x in readjsonfile("/home/kristian/projects/kraken-bash/ohlc.json")]
    y = [y[1] for y in readjsonfile("/home/kristian/projects/kraken-bash/ohlc.json")]

    z = np.polyfit(x, y, 2)
    f = np.poly1d(z)

    x_new = np.linspace(x[0], x[-1], 50)
    y_new = f(x_new)

    plt.plot(x,y,'o', x_new, y_new)
    plt.ylabel('Price in EURO')
    plt.show()

if __name__ == "__main__":
    plot()
