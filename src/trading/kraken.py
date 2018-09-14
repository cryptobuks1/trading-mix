import krakenex
from pykrakenapi import KrakenAPI
from trading.sql import memdb
import logging
from os.path import expanduser

def credentials(separator = '='):
    result_dict = {}
    with open(expanduser('~/.kraken')) as f:
        for line in f:
            parts = line.split(separator, 1)
            result_dict[parts[0]] = parts[1].rstrip()
    return result_dict


creds_dict = credentials()

api = krakenex.API(creds_dict['APIKEY'],
                   creds_dict['PRIVATEKEY'])
k = KrakenAPI(api)


def connect():
    api = krakenex.API(creds_dict['APIKEY'],
                   creds_dict['PRIVATEKEY'])
    k = KrakenAPI(api)
    return k


def get_rate():
    return k.get_ohlc_data("XXMRZEUR")


def to_sql(panda, table_name, **kwargs):
    env = kwargs.copy()
    if 'connection' not in env:
        env.update(memdb())
    con = env['connection']
    panda.to_sql(table_name, con, index=False)
    return con


def get_orders(**kwargs):
    orders, matches_cnt = k.get_trades_history()
    return to_sql(orders, 'orders', **kwargs)

def get_orders_between(start, end):
    k = connect()
    orders, _ = k.get_trades_history()
    return orders[orders['time'].between(start, end)]


def get_latest_order_epoc(**kwargs):
    if 'kraken' in kwargs.keys():
        k = kwargs['kraken']
    else:
        k = connect()
    orders, _ = k.get_trades_history()
    return orders.iloc[0].time


def get_currency_balance(currency='ZEUR', **kwargs):
    k = connect()
    balance_panda = k.get_account_balance()
    return balance_panda.loc[currency]['vol']


def ohlc(**kwargs):
    try:
        ohlc, last = get_rate()
    except Exception as e:
        print("Exception")
        print(e)
    return to_sql(ohlc, 'ohlc', **kwargs)


orders_table = "orders"
ohlc_table = "ohlc"
table_mapping = {orders_table: {"table": orders_table,
                                "time_column": "timestamp"},
                 ohlc_table: {"table": ohlc_table,
                              "time_column": "time",
                              "data_column": "open"}}


def create_order(command, amount):
    k = connect()
    logging.warn(command)
    return k.add_standard_order("XMREUR", command, 'market', str(amount), validate=False)
