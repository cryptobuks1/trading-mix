import logging
from trading.events import tradingEvents, emit
from trading.core import advice


def create():
    pass


def check_peak(is_new_peak_fn, data):
    logging.debug("Got Peak")
    if is_new_peak_fn(data['result']):
        tradingEvents.newPeak.send(check_peak, peak_analysis=data['result'])


def trigger_trade_advise(peak_analysis):
    logging.debug('Trade advice')
    emit(tradingEvents.advice, advice(peak_analysis))


def processAdvice(commands, advice):
    (commands[advice])()
