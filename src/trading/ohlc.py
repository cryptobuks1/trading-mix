import json
import matplotlib.dates as mdates
import datetime
import matplotlib.pyplot as plt

def readjsonfile(path):
    with open(path) as fo:
        ohlcjsonstring=fo.read()
        ohlcjson=json.loads(ohlcjsonstring)
        for record in ohlcjson["result"]["XXMRZEUR"]:
            yield [float(pair[1]) if pair[0]==1 else pair[1] for pair in enumerate(record)]
