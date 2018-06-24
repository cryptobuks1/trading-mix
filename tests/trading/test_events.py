from blinker import signal


def test_event_dispatch():
    event = signal('event')
    event.connect(lambda sender: print("recieved"))
    event.send('hest')
