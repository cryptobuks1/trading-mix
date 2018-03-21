import json


def readjsonfile(path):
    with open(path) as fo:
        ohlcjsonstring = fo.read()
        ohlcjson = json.loads(ohlcjsonstring)
        for record in ohlcjson["result"]["XXMRZEUR"]:
            yield [float(pair[1]) if pair[0] == 1 else pair[1] for pair in enumerate(record)]


def load(path):
    return [record for record in readjsonfile(path)]


def join_data(accumList, currentList):
    if not accumList:
        return currentList
    latest = accumList[-1][0]
    newData = [x for x in currentList if x[0] > latest]
    accumList.extend(newData)
    return accumList

def join(dataLists):
    sortedData = sorted(dataLists, key=lambda dl: dl[0][0])
    print sortedData[0][0]
    return reduce(join_data, sortedData, [])
