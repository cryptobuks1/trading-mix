from trading.octave import conf as peakConf
from trading.events import tradingEvents
from trading.events import bind
from trading.data import analyseData, is_new_peak
from trading.core import TradeCommand
from trading.strategy.simple import check_peak, trigger_trade_advise
from trading.strategy.simple import processAdvice, run
from functools import partial
import pytest
import logging

buy = 'BUY!!'
sell = 'SELL!!'

tradeCommands = {
    TradeCommand.sell: lambda: logging.debug(sell),
    TradeCommand.buy: lambda: logging.debug(buy)
}


@pytest.mark.newpeak
def test_new_high_peak(high_peak, high_peak_order_epoc, caplog):
    with caplog.at_level(logging.DEBUG):
        run(high_peak_order_epoc, tradeCommands, high_peak['data'])
    assert sell in caplog.text


@pytest.mark.newpeak
def test_new_low_peak(low_peak, low_peak_order_epoc, caplog):
    with caplog.at_level(logging.DEBUG):
        run(low_peak_order_epoc, tradeCommands, low_peak['data'])
    assert buy in caplog.text
