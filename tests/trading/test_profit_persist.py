
from trading.core import TradeCommand
from trading.data import window_generator
from trading.util import toDate
from trading.storage import save, load
from strategy_helper import take
import pytest
import logging


@pytest.mark.profit_persist
def test_profit(all_data, caplog):
    newMoney = 0
    euros = 0
    xmrs = 0
    rate = -1

    topic = "trading"
    state = load(topic)
    if not state:
        state = {}
        firstOrder = True


    def sell(analysis):
        nonlocal euros, xmrs, rate, firstOrder, newMoney, state
        rate = analysis['y'][-1]
        if firstOrder:
            firstOrder = False
            logging.warn("Selling on first order")
            newMonero = 5
            xmrs = 5
            euros = 0

            state['newMonero'] = state['newMonero'] + 5
            state['xmrs'] = 5
        euros += xmrs * rate
        logging.warn("at {} selling: {} xmr at rate {} for {} euros".format(toDate(analysis['x'][-1]), xmrs, rate, euros))
        xmrs = 0
        # sell here
        state['xmrs'] = 0
        state['euros'] = state['euros'] * rate
        save(state)

    def buy(analysis):
        nonlocal euros, xmrs, rate, firstOrder, newMoney, state
        rate = analysis['y'][-1]
        if euros == 0:
            firstOrder = False
            extraMoney = 5 * rate
            newMoney =+ extraMoney
            euros = extraMoney
            state['euros'] = 5 * rate
            state['newMoney'] = state['newMoney'] + state['euros']

        xmrs += euros / rate
        logging.warn("at {} buying: {} xmr at rate {} for {} euros".format(toDate(analysis['x'][-1]), xmrs, rate, euros))
        euros = 0

    tradeCommands = {
        TradeCommand.sell: sell,
        TradeCommand.buy: buy
    }

    run, events = take(7,
                       tradeCommands,
                       window_generator(3600 * 4,
                                        600,
                                        **all_data))
    # with caplog.at_level(logging.DEBUG):
    run()
    currentValueInEUROS = (xmrs * rate) + euros
    logging.warn("portfolio value {}".format(currentValueInEUROS - newMoney))
    logging.warn("Money {}".format(newMoney))
    assert  False
    #assert (xmrs * rate) + euros > newMoney * 3
