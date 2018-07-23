import logging
from trading.events import tradingEvents, emit
from trading.core import advice
from trading.data import is_new_peak, analyseData
from trading.events import bind
from trading.octave import conf as peakConf
from functools import partial


def run(latest_order_epoc, tradeCommands, data):
    def onPeak(**kwargs):
        check_peak(partial(is_new_peak, latest_order_epoc), **kwargs)

    bind(tradingEvents.foundPeak, onPeak)
    bind(tradingEvents.newPeak, trigger_trade_advise)
    bind(tradingEvents.advice, partial(processAdvice, tradeCommands))
    analyseData(peakConf, data,
                foundPeakEvent=tradingEvents.foundPeak)


def check_peak(is_new_peak_fn, data):
    logging.debug("Got Peak")
    if is_new_peak_fn(data['result']):
        tradingEvents.newPeak.send(check_peak, peak_analysis=data['result'])


def trigger_trade_advise(peak_analysis):
    logging.debug('Trade advice')
    emit(tradingEvents.advice, advice(peak_analysis))


def processAdvice(commands, advice):
    (commands[advice])()
