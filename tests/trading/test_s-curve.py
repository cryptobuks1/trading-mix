from trading.data import window,extract
from trading.sql import sqlite_connect
from trading.plot import axis_with_dates_x
import matplotlib.pyplot as plt
import numpy as np
from os.path import join
import pytest
import logging
import datetime
import time
from scipy.optimize import curve_fit


def func(x, a, b, c, d):
    return (a + b * x
            + c * x ** 2
            + d * x ** 3)


@pytest.mark.s_curve
def test_s_curve(data_dir, caplog):
    start = datetime.datetime(2018, 8, 21, 21, 00)
    start_epoc = start.timestamp()
    end = datetime.datetime(2018, 8, 21, 23, 12)
    end_epoc = end.timestamp()
    fig, ax = axis_with_dates_x()
    db = sqlite_connect(join(data_dir,
                             "ohcl-2018-08-22-00:17:13.sqlite"))
    curve = []
    with caplog.at_level(logging.DEBUG):
        data = extract(window(db['connection'],
                              **{**db,
                                 **{"start": start_epoc,
                                    "end": end_epoc}}))
        x = np.array(data[0])
        half = int(len(x)/2)
        quart = int(half/2)
        y = np.array(data[1])
        y = y - min(y)
        xsel = np.array([x[0], x[quart], x[half], x[-1]])
        ysel = np.array([y[0], y[quart], y[half], y[-1]])
        popt, _ = curve_fit(func, xsel, ysel)
        z = np.polyfit(**{"x": x,
                          "y": y,
                          "deg": 2})
        p = np.poly1d(z)
        xnew = np.linspace(x[0], x[-1], 500)
        xnd = [datetime.datetime.fromtimestamp(x) for x in xnew]
        xd = [datetime.datetime.fromtimestamp(x_) for x_ in x]
        ax.set_xlim(xd[0], xd[-1])

        ax.plot(xd, y, xnd, p(xnew))
        ax.plot([datetime.datetime.fromtimestamp(x) for x in xsel], func(xsel, *popt), 'r-')

        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(15)
        assert popt == p
