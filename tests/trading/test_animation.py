import matplotlib.pyplot as plt
import matplotlib.animation as animation
from trading.data import window_generator, analyseData
from trading.sql import connect
from trading.kraken import table_mapping, orders_table
from trading.plot import pause_frame_generator
from trading.octave import conf as peakConf
from trading.misc import desctructDict
from os.path import join
from functools import partial

def init(plots, ax):
    ticks, fitted, psl = ax.plot([],
                                 [],
                                 [],
                                 [],
                                 [],
                                 [], 'b+')
    plots['ticks'] = ticks
    plots['fitted'] = fitted
    plots['psl'] = psl
    return ticks, fitted, psl


def update(frame, plots, ax, state):
    ticks, fitted, psl = desctructDict(plots, ('ticks',
                                               'fitted',
                                               'psl'))
    result = analyseData(peakConf, frame)
    xs, ys, xfit, yfit, xpeak, ypeak, trade = desctructDict(result,
                                                            ("x",
                                                             "y",
                                                             "xfit",
                                                             "yfit",
                                                             "xpeak",
                                                             "ypeak",
                                                             "tradeAdvise"))
    ax.set_xlim(min(xs), max(xs))
    ax.set_ylim(min(ys), max(ys))
    ticks.set_data(xs, ys)
    fitted.set_data(xfit, yfit)
    psl.set_data(xpeak, ypeak)
    if xpeak:
        print(trade)
        state["continue"] = False
    return ticks, fitted, psl


state = {"continue": True}
def test_animation():
    global state
    db = connect("sqlite:///" + join('/home/kristian/projects/trading/data',
                                     'alldata.sqlite'))
    env = {**db, **table_mapping[orders_table]}
    fig, ax = plt.subplots()
    plots = {}

    init_fn = partial(init, plots, ax)
    frame_fn = pause_frame_generator(state, window_generator(3600 * 3, 600, **env))
    ani = animation.FuncAnimation(fig, update, frame_fn, init_fn, (plots, ax, state))
    plt.show(block=False)
