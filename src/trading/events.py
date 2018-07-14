from blinker import signal
from collections import namedtuple
from trading.misc import is_sequence

TradingEvents = namedtuple('TradingEvents', ['foundPeak', 'noPeak', 'newPeak'])
tradingEvents = TradingEvents(signal('foundPeak'),
                              signal('noPeak'),
                              signal('newPeak'))


DefaultEventBindings = namedtuple('EventBindings', TradingEvents._fields)
bindings = [[] for x in DefaultEventBindings._fields]
defaultEventBindings = DefaultEventBindings(*bindings)


def bindEvents(events, bindings):
    for key in events._fields:
        event = getattr(events, key)
        binding = getattr(bindings, key)
        if callable(binding):
            event.connect(binding)
        elif is_sequence(binding):
            for b in binding:
                print("seq")
                event.connect(b)
        else:
            raise Exception('Illegal binding')
