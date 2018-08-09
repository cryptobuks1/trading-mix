from trading.core import TradeCommand
from trading.data import window_generator
import pytest


from strategy_helper import take


tradeCommands = {
    TradeCommand.sell: lambda: True,
    TradeCommand.buy: lambda: True
}


@pytest.mark.profit
def test_profit(all_data):
    euros = 1000
    xmrs = 5
    take(4,
         tradeCommands,
         window_generator(3600 * 3,
                          600,
                          **all_data))
    assert xmrs > 5 or euros > 1000
