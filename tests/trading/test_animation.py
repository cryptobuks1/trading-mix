import matplotlib.pyplot as plt
import matplotlib.animation as animation
from trading.data import window_generator, pause_frame_generator
from trading.data import analyseData
from trading.sql import connect
from trading.kraken import table_mapping, orders_table
from trading.octave import conf as peakConf
from trading.recorder import record_event
from trading.events import tradingEvents
from trading.plot import axis_with_dates_x, update_with_fit_and_peak
from trading.plot import init_with_fit_and_peak
from trading.ui import show_control_window
from blinker import signal
from os.path import join
from functools import partial
import pytest


def onFoundPeak(state, sender, data):
    state['continue'] = False


def onNoPeak(state, sender, data):
    print("No peak")
    state['continue'] = False


def controlPlot(state, play=True):
    state['continue'] = not state['continue']


state = {"continue": True}

@pytest.mark.animation
def test_animation():
    global state
    db = connect("sqlite:///" + join('/home/kristian/projects/trading/data',
                                     'alldata.sqlite'))
    env = {**db, **table_mapping[orders_table]}
    fig, ax = axis_with_dates_x()
    plots = {}

    onFoundPeak_fn = partial(onFoundPeak, state)
    onNoPeak_fn = partial(onNoPeak, state)

    # def onFoundPeak_fn(data):
    #     onFoundPeak(state, data)
    event = tradingEvents.foundPeak
    event.connect(onFoundPeak_fn)
    npevent = tradingEvents.noPeak
    npevent.connect(onNoPeak_fn)
    recordEvent = signal('record')
    recordData_fn, persistData_fn = record_event(event, recordEvent)

    init_fn = partial(init_with_fit_and_peak, plots, ax)
    frame_fn = pause_frame_generator(state,
                                     window_generator(3600 * 3,
                                                      600,
                                                      **env))
    ani = animation.FuncAnimation(fig,
                                  partial(update_with_fit_and_peak,
                                          partial(analyseData,
                                                  peakConf)),
                                  frame_fn,
                                  init_fn,
                                  (plots, ax))
    # plt.show(block=False)
    # plt.show()
    top = Tk()
    top.geometry("150x100")

