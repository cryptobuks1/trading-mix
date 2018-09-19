import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.animation as animation
from trading.misc import desctructDict
from datetime import datetime
from functools import partial

def axis_with_dates_x():
    plt.ion()
    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    return fig, ax


def update_with_fit_and_peak(analysis_fns, frame, plots, ax):
    ticks, fitted, psl = desctructDict(plots, ('ticks',
                                               'fitted',
                                               'psl'))
    result = analysis_fns(frame)
    xs, ys, xfit, yfit, xpeak, ypeak = desctructDict(result,
                                                     ("x",
                                                      "y",
                                                      "xfit",
                                                      "yfit",
                                                      "xpeak",
                                                      "ypeak"))
    xd = [datetime.fromtimestamp(x) for x in xs]
    xfd = [datetime.fromtimestamp(x) for x in xfit]
    xpd = [datetime.fromtimestamp(x) for x in xpeak]
    ax.set_xlim(min(xd), max(xd))
    ax.set_ylim(min(ys), max(ys))
    ticks.set_data(xd, ys)
    fitted.set_data(xfd, yfit)
    psl.set_data(xpd, ypeak)
    return ticks, fitted, psl


def update_plot_with_fit_and_peak(plots, ax, analysis):
    ticks, fitted, psl = [plots[graph] for graph in ("ticks",
                                                     "fitted",
                                                     "psl")]
    xd = [datetime.fromtimestamp(x) for x in analysis['x']]
    xfd = [datetime.fromtimestamp(x) for x in analysis['xfit']]
    xpd = [datetime.fromtimestamp(x) for x in analysis['xpeak']]
    ticks.set_data(xd, analysis['y'])
    fitted.set_data(xfd, analysis['yfit'])
    psl.set_data(xpd, analysis['ypeak'])



def as_dates(xs):
    return [datetime.fromtimestamp(x) for x in xs]


def init_with_fit_and_peak(plots, ax):
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


def create_plot_with_fit_and_peak(analysis_fns, frame_fn, **kwargs):
    '''Create animation of analysis
    Args:
    **animation_interval (int): in milliseconds
    '''
    fig, ax = axis_with_dates_x()
    plots = {}
    init_fn = partial(init_with_fit_and_peak, plots, ax)
    interval = kwargs.get("animation_interval", 2000)
    return fig, ax, animation.FuncAnimation(fig,
                                            partial(update_with_fit_and_peak,
                                                    analysis_fns),
                                            frame_fn,
                                            init_fn,
                                            (plots, ax),
                                            interval=interval)


def plot_analysis(ax, analysis):
    ax.clear()
    ax.plot([datetime.fromtimestamp(x) for x in analysis['x']], analysis['y'])
    ax.plot([datetime.fromtimestamp(x) for x in analysis['xfit']], analysis['yfit'])
    # ax.plot([datetime.fromtimestamp(x) for x in analysis['xpeak']], analysis['ypeak'], 'b+')
    ax.axvline(x=datetime.fromtimestamp(analysis['xpeak'][0]), color='#ff0000')
