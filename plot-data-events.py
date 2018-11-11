sqlfile="/home/kristian/projects/trading/data/ohcl-2018-08-21-22:22:09.sqlite"
from trading.sql import sqlite_connect
from trading.data import (window_generator,
                          analyseData,
                          is_new_peak,
                          extract)
from trading.events import bind, emit
from trading.octave import conf as peakConf
from trading.control import setup_analysis
from trading.plot import as_dates, update_graph
from functools import partial
from dev.order import simulation
import logging
logging.basicConfig(level=logging.DEBUG)



db = sqlite_connect(sqlfile)


data_analysis = setup_analysis(window_generator(3600 * 3,
                                                600,
                                                **db))
sim = simulation()


def onPeak(get_latest_order_epoc, newPeakEvent, data):
    if is_new_peak(get_latest_order_epoc, data['result']):
        emit(newPeakEvent,
             data={"peak_analysis": data['result']},
             unpack_data=True)


def plot_peak(fig, graph, data):
    update_graph(fig,
                 graph,
                 as_dates(data['result']['xfit']),
                 data['result']['yfit'])


def plot_new_peak(fig, graph, peak_analysis):
    update_graph(fig,
                 graph,
                 as_dates(peak_analysis['xpeak']),
                 peak_analysis['ypeak'])


def plot_data(fig, graph, data):
    x, y = extract(data)
    xd = as_dates(x)
    data_analysis.ax.set_xlim(min(xd), max(xd))
    data_analysis.ax.set_ylim(min(y), max(y))
    update_graph(fig,
                 graph,
                 xd,
                 y)


bind(data_analysis.events.data,
     partial(plot_data,
             data_analysis.fig,
             data_analysis.default_plots.ticks))

bind(data_analysis.events.data,
     partial(analyseData,
             peakConf,
             foundPeakEvent=data_analysis.events.foundPeak))

bind(data_analysis.events.foundPeak,
     partial(plot_peak,
             data_analysis.fig,
             data_analysis.default_plots.fitted))

bind(data_analysis.events.newPeak,
     partial(plot_new_peak,
             data_analysis.fig,
             data_analysis.default_plots.psl))

sim.trade_on_peak(data_analysis.events.newPeak)

bind(data_analysis.events.newPeak,
     lambda peak_analysis: data_analysis.pause_graph())

bind(data_analysis.events.foundPeak,
     partial(onPeak,
             sim.get_latest_order_epoc,
             data_analysis.events.newPeak))

data_analysis.run()
