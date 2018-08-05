import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from trading.misc import desctructDict
from datetime import datetime


def axis_with_dates_x():
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
