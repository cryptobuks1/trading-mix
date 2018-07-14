from blinker import signal
from functools import partial
from trading.recorder import record_event
from trading.misc import is_sequence
from collections import namedtuple


def static_fn(sender):
    print(sender)


def static_data_fn(data, sender):
    print(data)


def test_event_dispatch():
    event = signal('event')
    event.connect(static_fn)

    def internal_fn(sender):
        print('internal')

    event.connect(internal_fn)

    lmd = lambda sender: print("lmd")
    event.connect(lmd)

    part = partial(static_data_fn, 'data')
    event.connect(part)

    event.connect(lambda sender: print("inline lambda"))
    event.connect(partial(static_data_fn, 'inline partial'))
    event.send('hest')


def test_sub_part():
    dataEvent = signal('dataEvent')
    recordEvent = signal('recordEvent')
    f1, f2 = record_event(dataEvent, recordEvent)
    dataEvent.send('data', data='hjort')
    recordEvent.send('record')


foundPeakEvent = 'foundPeak'
noPeakEvent = 'noPeak'
newPeakEvent = 'newPeak'
TradingEvents = namedtuple('TradingEvents', ['foundPeak', 'noPeak', 'newPeak'])
tradingEvents = TradingEvents(signal('foundPeak'),
                              signal('noPeak'),
                              signal('newPeak'))


DefaultEventBindings = namedtuple('EventBindings', TradingEvents._fields)
bindings = [[] for x in DefaultEventBindings._fields]
defaultEventBindings = DefaultEventBindings(*bindings)


def reaction(sender, data):
    print(data)


def reaction2(sender, data):
    print("sender", data)


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
