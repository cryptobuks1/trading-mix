from trading.core import TradeCommand
import pytest
import logging


from strategy_helper import take


tradeCommands = {
    TradeCommand.sell: lambda: True,
    TradeCommand.buy: lambda: True
}

@pytest.mark.profit
def test_profit(all_data):
    take(20, tradeCommands, **all_data)
