import logging
from trading.events import tradingEvents


def create():
    pass


def check_peak(is_new_peak_fn, data):
    logging.debug("Got Peak")
    if is_new_peak_fn(data['result']):
        tradingEvents.newPeak.send(check_peak, peak_analysis=data['result'])
