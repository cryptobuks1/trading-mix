import warnings
warnings.filterwarnings("ignore", message="numpy.dtype size changed")
from trading.core import default_kraken_strategy
from trading.sql import memdb, time_range
from trading.kraken import ohlc, get_latest_order_epoc, create_order
from trading.events import TradingEvents, bind
import logging
from datetime import datetime
import pickle
from os.path import expanduser, exists, dirname
from os import makedirs

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)-8s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


def main():
    store_data_p = False

    def buy(analysis):
        nonlocal store_data_p
        store_data_p = True
        create_order('buy', 5)

    def sell(analysis):
        nonlocal store_data_p
        store_data_p = True
        create_order('sell', 5)

    [strategy,
     events] = default_kraken_strategy(**{"buy_fn":
                                          buy,
                                          "sell_fn":
                                          sell,
                                          "latest_order_epoc_fn":
                                          get_latest_order_epoc,
                                          "window_size":
                                          3600 * 5})
    db = memdb()
    ohlc(**db)
    start, end = time_range(**db)
    logging.debug(start)
    logging.warn(end)

    def store_data(data):
        date = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        data_path = expanduser('~/.local/lib/trading/data/order-data-' + date + '.sqlite')
        data_dir = dirname(data_path)
        if not exists(data_dir):
            makedirs(data_dir)
        with open(data_path, 'wb') as f:
            pickle.dump(data, f)

    ohlc_data = None

    def reference_data(data):
        nonlocal ohlc_data
        ohlc_data = data

    bind(TradingEvents.data.fget(events), lambda data: reference_data(data['data']))
    strategy(db)
    if store_data_p:
        store_data(ohlc_data)
        store_data_p = False



if __name__ == "__main__":
    main()
