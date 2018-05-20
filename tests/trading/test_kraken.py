import matplotlib.pyplot as plt
from trading.data import fit, extract, peaks
from trading.sql import window
from os import getenv
from os.path import join
import sqlite3


def press(event):
    print('press', event.key)

def test_animation():
    con = sqlite3.connect(join(getenv('DATA_DIR'), 'alldata.sqlite'))
    cur = con.cursor()
    fig, ax = plt.subplots()
    fig.canvas.mpl_connect('key_press_event', press)
    cur.execute("SELECT min(timestamp) FROM ohlc")
    start = int(cur.fetchall()[0][0])
    windowpos = start
    windowsize = 10800
    data = window(con, windowpos, windowpos + windowsize)
    xs, ys, x_new, y_new, f = fit(extract(data))
    ps = peaks(y_new)
    ax.plot(xs, ys)
    plt.show()
