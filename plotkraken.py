def ohlcFile():
    with open(path) as js:
        jsc=js.read(path)
        print jsc
        jsp=json.loads(jsc)
        print jsp["result"]["XXMRZEUR"]
        for record in jsp["result"]["XXMRZEUR"]:
            yield record

if __name__ == "__main__":
    for record in ohlcFile("/home/kristian/projects/kraken-bash/ohlc.json"):
        print record
