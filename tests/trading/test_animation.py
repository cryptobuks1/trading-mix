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
from trading.plot import create_plot_with_fit_and_peak
from trading.ui import show_control_window
from blinker import signal
from os.path import join
from functools import partial
import pytest
import logging


def onFoundPeak(state, sender, data):
    state['continue'] = False


def onNoPeak(state, sender, data):
    logging.warn("No peak")
    #state['continue'] = False


def controlPlot(state, play=True):
    state['continue'] = not state['continue']


state = {"continue": True}

@pytest.mark.animation
def test_animation(caplog):
    global state
    db = connect("sqlite:///" + join('/home/kristian/projects/trading/data',
                                     'ohcl-2018-08-22-07:41:50.sqlite'))
    # env = {**db, **table_mapping[orders_table]}
    env = db

    onFoundPeak_fn = partial(onFoundPeak, state)
    onNoPeak_fn = partial(onNoPeak, state)

    event = tradingEvents.foundPeak
    event.connect(onFoundPeak_fn)
    npevent = tradingEvents.noPeak
    npevent.connect(onNoPeak_fn)
    recordEvent = signal('record')
    recordData_fn, persistData_fn = record_event(event, recordEvent)

    frame_fn = pause_frame_generator(state,
                                     window_generator(3600 * 3,
                                                      600,
                                                      **env))
    analysis_fn = partial(analyseData,
                          peakConf)
    with caplog.at_level(logging.DEBUG):
        fig, ax, ani = create_plot_with_fit_and_peak(analysis_fn, frame_fn)
        plt.show(block=False)
        show_control_window(lambda: controlPlot(state),
                            recordEvent)
