sqlfile="/home/kristian/projects/trading/data/ohcl-2018-08-21-22:22:09.sqlite"
from trading.data import window_generator, TradeCommand, extract
from trading.plot import axis_with_dates_x, update_plot_with_fit_and_peak
from trading.plot import init_with_fit_and_peak
from functools import partial
from trading.strategy.simple import create_strategy
from trading.sql import sqlite_connect
from dev.order import simulation
from time import sleep
from datetime import datetime

fig, ax = axis_with_dates_x()
fig.patch.set_facecolor('white')

plots = {}
init_with_fit_and_peak(plots, ax)

db = sqlite_connect(sqlfile)

plotter = partial(update_plot_with_fit_and_peak, plots, ax)


def throw(message):
    raise Exception(message)

tradeCommands = {
    TradeCommand.sell: plotter,
    TradeCommand.buy: plotter
}

sim = simulation()

strategy, events = create_strategy(sim.get_latest_order_epoc, tradeCommands)
sim.trade_on_peak(events)
for data in window_generator(3600 * 5, 600, **db):
    x, y = extract(data)
    xd = [datetime.fromtimestamp(x_) for x_ in x]
    ax.set_xlim(min(xd), max(xd))
    ax.set_ylim(min(y), max(y))
    plots['ticks'].set_data(xd, y)
    fig.canvas.draw()
    fig.canvas.flush_events()
    strategy(data)
