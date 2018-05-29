import krakenex
from pykrakenapi import KrakenAPI


def get_rate():
    api = krakenex.API()
    k = KrakenAPI(api)
    return k.get_ohlc_data("XXMRZEUR")
