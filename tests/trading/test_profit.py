from trading.core import TradeCommand
from trading.data import window_generator
from trading.events import TradingEvents
from trading.events import bind
from trading.util import toDate
from trading.plot import axis_with_dates_x
from strategy_helper import take
from datetime import datetime
import matplotlib.pyplot as plt
import pytest
import logging


@pytest.mark.profit
def test_profit(all_data, caplog):
    newMoney = 0
    newXMR = 0
    euros = 0
    xmrs = 0
    rate = -1
    firstOrder = True

    fig, ax = axis_with_dates_x()

    def plotAnalysis(analysis):
        ax.plot([datetime.fromtimestamp(x) for x in analysis['x']],
                analysis['y'],
                [datetime.fromtimestamp(x) for x in analysis['xfit']],
                analysis['yfit'])
        ax.axvline(x=datetime.fromtimestamp(analysis['xpeak'][0]))

    def sell(analysis):
        nonlocal euros, xmrs, rate, firstOrder, ax, newMoney
        rate = analysis['y'][-1]
        plotAnalysis(analysis)
        if firstOrder:
            logging.warn("Selling on first order")
            extraMoney = 5 * rate
            newMoney += extraMoney
            xmrs = 5
            euros = 0
            firstOrder = False
        euros += xmrs * rate
        logging.warn("at {} selling: {} xmr at rate {} for {} euros".
                     format(toDate(analysis['x'][-1]), xmrs, rate, euros))
        xmrs = 0

    def buy(analysis):
        nonlocal euros, xmrs, rate, firstOrder, ax, newMoney
        rate = analysis['y'][-1]
        plotAnalysis(analysis)
        if euros == 0:
            extraMoney = 5 * rate
            newMoney += extraMoney
            euros = extraMoney
            firstOrder = False

        xmrs += euros / rate
        logging.warn("at {} buying: {} xmr at rate {} for {} euros".
                     format(toDate(analysis['x'][-1]), xmrs, rate, euros))
        euros = 0

    tradeCommands = {
        TradeCommand.sell: sell,
        TradeCommand.buy: buy
    }

    run, events = take(7,
                       tradeCommands,
                       window_generator(3600 * 3,
                                        300,
                                        **all_data))
    with caplog.at_level(logging.DEBUG):
        run()
    currentValueInEUROS = (xmrs * rate) + euros
    logging.warn("portfolio value {}".format(currentValueInEUROS - newMoney))
    logging.warn("Money {}".format(newMoney))
    plt.show()
    assert False
