import matplotlib.pyplot as plt
import matplotlib.animation as animation
from trading.data import fit, extract, peaks
from trading.sql import window
from os import getenv
from os.path import join
import sqlite3
from flask import Flask
app = Flask(__name__)
con = sqlite3.connect(join(getenv('DATA_DIR'), 'alldata.sqlite'))
cur = con.cursor()


def press(event):
    print('press', event.key)

windowpos = 0
windowsize = 10800


@app.route('/windowpos/<int:pos>')
def setwindowpos(pos):
    global windowpos
    windowpos = pos
    return 'OK'

ticks, fitted, psl = [], [], []
ax = False


def init():
    global ticks, fitted, psl,windowpos, windowsize
    data = window(con, windowpos, windowpos + windowsize)
    xs, ys, x_new, y_new, f = fit(extract(data))
    ps = peaks(y_new)
    ticks.set_data(xs, ys)
    fitted.set_data(x_new, y_new)
    psl.set_data(x_new[ps], y_new[ps])
    return ticks, fitted, psl

def data_gen(t = 0):
    global windowpos, windowsize
    while True:
        yield window(con, windowpos, windowpos + windowsize)


def run(data):
    global ticks, fitted, psl,ax
    xs, ys, x_new, y_new, f = fit(extract(data))
    ax.set_xlim(min(xs), max(xs))
    ax.set_ylim(min(ys), max(ys))
    ax.grid(True)
    ax.figure.canvas.draw()
    ps = peaks(y_new)
    ticks.set_data(xs, ys)
    fitted.set_data(x_new, y_new)
    psl.set_data(x_new[ps], y_new[ps])
    return ticks, fitted, psl

def test_animation():
    global windowpos, ticks, fitted, psl, ax
    fig, ax = plt.subplots()
    fig.canvas.mpl_connect('key_press_event', press)
    cur.execute("SELECT min(timestamp) FROM ohlc")
    start = int(cur.fetchall()[0][0])
    windowpos = start
    windowsize = 10800
    data = window(con, windowpos, windowpos + windowsize)
    xs, ys, x_new, y_new, f = fit(extract(data))
    ps = peaks(y_new)
    ticks, fitted, psl = ax.plot(xs, ys, x_new, y_new,x_new[ps], y_new[ps])

    ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=500,
                                  repeat=False, init_func=init)

    plt.show(block = False)
    #start_server()


def start_server():
    app.run()


def stop_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
