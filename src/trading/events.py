from blinker import signal, Signal
from collections import namedtuple
from trading.misc import is_sequence, throw

TradingEvents = namedtuple('TradingEvents', ['foundPeak',
                                             'noPeak',
                                             'newPeak',
                                             'tradeAdvise',
                                             'advice',
                                             'data'])

tradingEvents = TradingEvents(*[signal(k) for k in TradingEvents._fields])


def create_trading_events():
    return TradingEvents(*[Signal() for k in TradingEvents._fields])


class BindError(Exception):
    pass


def bind(event, subscriber, includeSender=False, keep_ref=True):
    def strip_senders(sender, **kwargs):
        subscriber(**kwargs)

    sender = True
    ref = True
    argument_error = '''The combination: includeSender=False, keep_ref=False
    is not allowed. Reference must be kept past scope end for bind'''
    cases = {
        (sender, ref):
        lambda: event.connect(subscriber, weak=False),
        (sender, not ref):
        lambda: event.connect(subscriber),
        (not sender, ref):
        lambda: event.connect(strip_senders, weak=False),
        (not sender, not ref):
        lambda: throw(BindError(argument_error))
    }
    cases[(includeSender, keep_ref)]()


def emit(event, data=None, sender='anonymous', **kwargs):
    unpack_data = kwargs.get("unpack_data", False)
    if data:
        if not unpack_data:
            event.send(sender, **{'data': data})
        else:
            event.send(sender, **data)
    else:
        event.send(sender)
