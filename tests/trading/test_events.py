from blinker import signal
from functools import partial
from trading.recorder import record_event

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
    event.send('hest')


def test_sub_part():
    dataEvent = signal('dataEvent')
    recordEvent = signal('recordEvent')
    f1, f2 = record_event(dataEvent, recordEvent)
    dataEvent.send('data', data='hjort')
    recordEvent.send('record')
