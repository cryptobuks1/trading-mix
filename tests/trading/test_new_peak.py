from trading.core import TradeCommand
from trading.strategy.simple import create
import pytest
import logging

buy = 'BUY!!'
sell = 'SELL!!'

tradeCommands = {
    TradeCommand.sell: lambda: logging.debug(sell),
    TradeCommand.buy: lambda: logging.debug(buy)
}


@pytest.mark.regression
@pytest.mark.newpeak
def test_new_high_peak(high_peak, high_peak_order_epoc, caplog):
    with caplog.at_level(logging.DEBUG):
        engine, events = create(high_peak_order_epoc,
                                tradeCommands)
        # Testing octave with no extra parameters
        engine(high_peak['data'], ** {'peak_params': ()})
    assert sell in caplog.text


@pytest.mark.regression
@pytest.mark.newpeak
def test_new_low_peak(low_peak, low_peak_order_epoc, caplog):
    with caplog.at_level(logging.DEBUG):
        engine, events = create(low_peak_order_epoc,
                                tradeCommands)
        engine(low_peak['data'])
    assert buy in caplog.text
