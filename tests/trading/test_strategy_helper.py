from trading.core import TradeCommand
from trading.data import window_generator
from trading.events import TradingEvents
from trading.events import bind
from strategy_helper import take
import pytest
import logging


@pytest.mark.strategyhelper
def test_strategy_helper(all_data):
    tradeCommands = {
        TradeCommand.sell: lambda: True,
        TradeCommand.buy: lambda: True
    }

    run, events = take(4,
                       tradeCommands,
                       window_generator(3600 * 3,
                                        600,
                                        **all_data))
    bind(TradingEvents.newPeak.fget(events),
         lambda peak_analysis: logging.warn("Current rate {}".format(peak_analysis['y'][-1])))
    run()
    assert False
