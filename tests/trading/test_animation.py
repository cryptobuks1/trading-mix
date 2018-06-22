import matplotlib.pyplot as plt
import matplotlib.animation as animation
from trading.data import window_generator, pause_frame_generator
from trading.data import analyseData, foundPeakEvent
from trading.sql import connect
from trading.kraken import table_mapping, orders_table
from trading.octave import conf as peakConf
from trading.misc import desctructDict
from blinker import signal
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


def update(frame, plots, ax):
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
    return ticks, fitted, psl


def onFoundPeak(state, sender, data):
    state['continue'] = False


def test_animation():
    db = connect("sqlite:///" + join('/home/kristian/projects/trading/data',
                                     'alldata.sqlite'))
    env = {**db, **table_mapping[orders_table]}
    fig, ax = plt.subplots()
    plots = {}

    state = {"continue": True}
    onFoundPeak_fn = partial(onFoundPeak, state)

    # def onFoundPeak_fn(data):
    #     onFoundPeak(state, data)
    event = signal(foundPeakEvent)
    event.connect(onFoundPeak_fn)

    init_fn = partial(init, plots, ax)
    frame_fn = pause_frame_generator(state,
                                     window_generator(3600 * 3,
                                                      600,
                                                      **env))
    ani = animation.FuncAnimation(fig, update, frame_fn, init_fn, (plots, ax))
    # plt.show(block=False)
    plt.show()
    print(ani)
