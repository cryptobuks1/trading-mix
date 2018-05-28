import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from trading.data import fit, extract, peaks
from trading.sql import window
from os import getenv
from os.path import join
import sqlite3
from flask import Flask
from oct2py import octave
# from werkzeug.serving import run_simple

app = Flask(__name__)
print(join('/home/kristian/projects/trading/data', 'alldata.sqlite'))
con = sqlite3.connect(join('/home/kristian/projects/trading/data',
                           'alldata.sqlite'))
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
goon = True

def init():
    global ticks, fitted, psl,windowpos, windowsize
    data = window(con, windowpos, windowpos + windowsize)
    xs, ys, x_new, y_new, f = fit(extract(data))
    ps = peaks(y_new)
    ticks.set_data(xs, ys)
    fitted.set_data(x_new, y_new)
    psl.set_data(x_new[ps], y_new[ps])
    return ticks, fitted, psl


def data_gen(t=0):
    global windowpos, windowsize
    while True:
        yield window(con, windowpos, windowpos + windowsize)


last_peak = -1


def new_peakP(plist, y_new, valuepos=0, idxpos=1):
    print(plist[idxpos])
    new_peak = False
    if plist[valuepos] and not abs(last_peak - plist[0][0]) <= 5:
        print(last_peak)
        print(plist[0][0])
        new_peak = True
    return new_peak


def transform(i):
    print(i)
    return int(i)


def run(data):
    global ticks, fitted, psl, ax, goon, windowpos, last_peak

    xs, ys, x_new, y_new, f = fit(extract(data))
    ax.set_xlim(min(xs), max(xs))
    ax.set_ylim(min(ys), max(ys))
    ax.grid(True)
    ax.figure.canvas.draw()
    ps = peaks(y_new)
    ps = octave.findpeaks(y_new, nout=2)
    if ps[1] and not isinstance(ps[1], list):
        ps = [[ps[0]], [ps[1]]]
    print(isinstance(ps[1], list))
    ps[1] = list(map(transform, ps[1]))

    if(new_peakP(ps, y_new)):
        print("New peak")
        last_peak = ps[0][0]
        goon = False
        psl.set_data(x_new[np.array(ps[1])], y_new[ps[1]])
    if goon:
        addmin(10)
    ticks.set_data(xs, ys)
    fitted.set_data(x_new, y_new)

    return ticks, fitted, psl


def addmin(m):
    global windowpos
    windowpos = windowpos + (m * 60)


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
    ticks, fitted, psl = ax.plot(xs,
                                 ys,
                                 x_new,
                                 y_new,
                                 x_new[ps],
                                 y_new[ps], 'b+')

    ani = animation.FuncAnimation(fig, run, data_gen, blit=False, interval=500,
                                  repeat=False, init_func=init)

    plt.show(block = False)
    #start_server()


def start_server():
    app.run()
    #run_simple('localhost', 5000, app, use_reloader=True)


def stop_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def goagain():
    global goon
    goon = True

def test_octave():
    cur.execute("SELECT min(timestamp) FROM ohlc")
    start = int(cur.fetchall()[0][0])
    print(start)
    windowpos = start + 3600
    windowsize = 10800
    data = window(con, windowpos, windowpos + windowsize)
    xs, ys, x_new, y_new, f = fit(extract(data))
    print(y_new)
    octave.eval("pkg load signal")
    pe = octave.findpeaks(y_new, 'DoubleSided', 'MinPeakHeight', 0.04,
                          'MinPeakDistance', 30, 'MinPeakWidth', 0)
    pe = octave.findpeaks(y_new, 'DoubleSided')
    ps = peaks(y_new)
    plt.plot(x_new, y_new)
    plt.show()
    print(ps)
    print(pe)
