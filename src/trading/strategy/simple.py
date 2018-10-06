# coding: utf-8

import logging
from trading.events import create_trading_events, emit
from trading.data import is_new_peak, analyseData, advice
from trading.events import bind
from trading.octave import conf as peakConf
from functools import partial
import inspect


analyzer = partial(analyseData, peakConf)


def create(latest_order_epoc, tradeCommands):
    tradingEvents = create_trading_events()

    bind(tradingEvents.foundPeak, partial(check_peak,
                                          tradingEvents,
                                          partial(is_new_peak,
                                                  latest_order_epoc)))
    bind(tradingEvents.newPeak, partial(trigger_trade_advise, tradingEvents))
    bind(tradingEvents.advice, partial(processAdvice, tradeCommands))

    def start(data, **kwargs):
        analyzer(data,
                 foundPeakEvent=tradingEvents.foundPeak,
                 **kwargs)

    return start, tradingEvents


create_strategy = create


def check_peak(tradingEvents, is_new_peak_fn, data, **kwargs):
    logging.debug("Got Peak")
    if is_new_peak_fn(data['result'], **kwargs):
        tradingEvents.newPeak.send(check_peak, peak_analysis=data['result'])


def trigger_trade_advise(tradingEvents, peak_analysis):
    tradeAdvice = advice(peak_analysis)
    logging.debug('Ƀ Trade advice {}'.format(tradeAdvice))
    emit(tradingEvents.advice, {'advice': tradeAdvice,
                                'analysis': peak_analysis})


def processAdvice(commands, data):
    logging.debug("Call callback")
    logging.debug(type(data['advice']))
    advice = data['advice']
    logging.debug(advice)
    for idx in commands.keys():
        logging.debug(idx)
        if advice == idx:
            logging.debug("Index found")
        logging.debug(type(idx))
        logging.debug(commands[idx])
    cmd = commands[data['advice']]
    if 0 == inspect.signature(cmd).parameters.keys():
        cmd()
    else:
        cmd(data['analysis'])
