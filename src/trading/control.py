from trading.events import create_trading_events
from trading.core import stream_data_to_graph
from trading.plot import (axis_with_dates_x,
                          plot_data_with_x_as_date,
                          get_default_plots)
from os.path import join
from collections import namedtuple
from functools import partial


def handleError(e):
    raise e


def writeData(dataDir, data):
    path = join(dataDir, )


def setup_analysis(window_generator):
    events = create_trading_events()
    (run,
     window,
     play_pause_handler) = stream_data_to_graph(window_generator,
                                                events)
    fig, ax = axis_with_dates_x()
    fig.patch.set_facecolor('white')
    default_plots = get_default_plots(ax)
    DataAnalysis = namedtuple("DataAnalysis", ["run",
                                               "events",
                                               "play_pause_handler",
                                               "fig",
                                               "ax",
                                               "default_plots",
                                               "window",
                                               "plot"])
    plot = partial(plot_data_with_x_as_date, fig, ax)
    return DataAnalysis(run,
                        events,
                        play_pause_handler,
                        fig,
                        ax,
                        default_plots,
                        window,
                        plot)
