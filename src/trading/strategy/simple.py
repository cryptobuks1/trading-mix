import logging
from trading.events import create_trading_events, emit
from trading.core import advice
from trading.data import is_new_peak, analyseData
from trading.events import bind
from trading.octave import conf as peakConf
from functools import partial


def create(latest_order_epoc, tradeCommands):
    tradingEvents = create_trading_events()

    bind(tradingEvents.foundPeak, partial(check_peak,
                                          tradingEvents,
                                          partial(is_new_peak,
                                                  latest_order_epoc)))
    bind(tradingEvents.newPeak, partial(trigger_trade_advise, tradingEvents))
    bind(tradingEvents.advice, partial(processAdvice, tradeCommands))

    def start(data, **kwargs):
        analyseData(peakConf, data,
                    foundPeakEvent=tradingEvents.foundPeak,
                    **kwargs)

    return start, tradingEvents


def check_peak(tradingEvents, is_new_peak_fn, data, **kwargs):
    logging.debug("Got Peak")
    if is_new_peak_fn(data['result']):
        tradingEvents.newPeak.send(check_peak, peak_analysis=data['result'])


def trigger_trade_advise(tradingEvents, peak_analysis):
    logging.debug('Trade advice')
    emit(tradingEvents.advice, advice(peak_analysis))


def processAdvice(commands, data):
    logging.debug("Call callback")
    (commands[data])()
