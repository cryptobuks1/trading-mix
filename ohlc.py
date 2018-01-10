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

if __name__ == "__main__":
    print [x[0] for x in readjsonfile("/home/kristian/projects/kraken-bash/ohlc.json")]
    #plt.plot([x[1] for x in ohlcFile("/home/kristian/projects/kraken-bash/ohlc.json")])
    # plt.plot_date(
    #     mdates.date2num([x[0] for x in ohlcFile("/home/kristian/projects/kraken-bash/ohlc.json")]),
    #     [x[1] for x in ohlcFile("/home/kristian/projects/kraken-bash/ohlc.json")]
    # )
