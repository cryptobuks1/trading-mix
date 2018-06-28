from functools import partial
import pickle
import tempfile


def recordData(store, sender, data):
    store['data'] = data


def persistData(store, sender):
    with tempfile.NamedTemporaryFile(prefix='pickle', delete=False) as f:
        print(pickle)
        pickle.dump(store['data'], f, pickle.HIGHEST_PROTOCOL)
        print(f.name)


def record_event(dataEvent, recordEvent):
    store = {}
    recordData_fn = partial(recordData, store)
    dataEvent.connect(recordData_fn)
    persistData_fn = partial(persistData, store)
    recordEvent.connect(persistData_fn)
    return recordData_fn, persistData_fn
