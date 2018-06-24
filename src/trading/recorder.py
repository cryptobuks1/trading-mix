from functools import partial


def recordData(store, sender, data):
    print("Record")
    store['data'] = data


def persistData(store, sender):
    print("persistData")
    print(store)


def record_event(dataEvent, recordEvent):
    store = {}
    recordData_fn = partial(recordData, store)
    dataEvent.connect(recordData_fn)
    persistData_fn = partial(persistData, store)
    recordEvent.connect(persistData_fn)
    return recordData_fn, persistData_fn
