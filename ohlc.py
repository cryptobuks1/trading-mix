import json
import matplotlib.dates as mdates
import datetime
import matplotlib.pyplot as plt

def ohlcFile(path):
    with open(path) as fo:
        ohlcjsonstring=fo.read()
        ohlcjson=json.loads(ohlcjsonstring)
        for record in ohlcjson["result"]["XXMRZEUR"]:
            record[0] = datetime.datetime.fromtimestamp(record[0])
            yield record

if __name__ == "__main__":
    print [x[0] for x in ohlcFile("/home/kristian/projects/kraken-bash/ohlc.json")]
    #plt.plot([x[1] for x in ohlcFile("/home/kristian/projects/kraken-bash/ohlc.json")])
    # plt.plot_date(
    #     mdates.date2num([x[0] for x in ohlcFile("/home/kristian/projects/kraken-bash/ohlc.json")]),
    #     [x[1] for x in ohlcFile("/home/kristian/projects/kraken-bash/ohlc.json")]
    # )
    plt.plot(
        [x[0] for x in ohlcFile("/home/kristian/projects/kraken-bash/ohlc.json")],
        [y[1] for y in ohlcFile("/home/kristian/projects/kraken-bash/ohlc.json")])
    plt.gcf().autofmt_xdate()
    plt.ylabel('Price in EURO')
    plt.show()

