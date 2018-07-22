from trading.octave import conf as peakConf
from trading.events import tradingEvents
from trading.events import bind, emit
from trading.data import analyseData
from trading.core import advice, TradeCommand
from functools import partial
import pytest
import logging

buy='BUY!!'
sell='SELL!!'

tradeCommands = {
    TradeCommand.sell: lambda: logging.debug(sell),
    TradeCommand.buy: lambda: logging.debug(buy)
}


def check_peak(latest_order_epoc, data):
    logging.debug("Got Peak")
    peakEpoc = data['result']['xpeak'][0]
    timeDiff = abs(peakEpoc - latest_order_epoc)
    if timeDiff < 1200:  # within 20 minutes
        tradingEvents.newPeak.send(check_peak, peak_analysis=data['result'])


def trigger_trade_advise(peak_analysis):
    logging.debug('Trade advice')
    emit(tradingEvents.advice, advice(peak_analysis))


def processAdvice(commands, advice):
    (commands[advice])()


@pytest.mark.newpeak
def test_new_high_peak(high_peak, high_peak_order_epoc, caplog):
    def onPeak(**kwargs):
        check_peak(high_peak_order_epoc, **kwargs)

    bind(tradingEvents.foundPeak, onPeak)
    bind(tradingEvents.newPeak, trigger_trade_advise)
    bind(tradingEvents.advice, partial(processAdvice, tradeCommands))
    with caplog.at_level(logging.DEBUG):
        analyseData(peakConf, high_peak['data'],
                    foundPeakEvent=tradingEvents.foundPeak)
    assert sell in caplog.text


@pytest.mark.newpeak
def test_new_low_peak(low_peak, low_peak_order_epoc, caplog):
    def onPeak(**kwargs):
        check_peak(low_peak_order_epoc, **kwargs)

    bind(tradingEvents.foundPeak, onPeak)
    bind(tradingEvents.newPeak, trigger_trade_advise)
    bind(tradingEvents.advice, partial(processAdvice, tradeCommands))
    with caplog.at_level(logging.DEBUG):
        analyseData(peakConf, low_peak['data'],
                    foundPeakEvent=tradingEvents.foundPeak)
    assert buy in caplog.text
