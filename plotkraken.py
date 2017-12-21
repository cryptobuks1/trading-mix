import json
def ohlcFile(path):
    with open(path) as fo:
        ohlcjsonstring=fo.read()
        ohlcjson=json.loads(ohlcjsonstring)
        for record in ohlcjson["result"]["XXMRZEUR"]:
            yield record

if __name__ == "__main__":
    for record in ohlcFile("/home/kristian/projects/kraken-bash/ohlc.json"):
        print record
