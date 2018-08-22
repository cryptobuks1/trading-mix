from trading.strategy.simple import create
from eventhelpers import update_order_with_peak
from trading.events import bind
from trading.core import default_kraken_strategy
import logging


def take(count, tradeCommands, gen):
    latest_order_epoc = {'epoc': 0}
    speaks = []

    engine, events = create(lambda: latest_order_epoc['epoc'],
                            tradeCommands)
    update_order_with_peak(events, latest_order_epoc)
    bind(events.newPeak,
         lambda peak_analysis: speaks.append(peak_analysis['xpeak'][0]))

    def run():
        nonlocal speaks, gen, engine
        for window in (w if len(speaks) < count
                       else (_ for _ in ()).throw(StopIteration())
                       for w in gen):
            engine(window)
    return run, events


def bindings_for_default_kraken_strategy(latest_order_epoc,
                                         window_size=3600 * 3):
    buyMessage = "buy ~~~"
    sellMessage = "sell ~~~"

    def buy(analysis):
        nonlocal buyMessage
        logging.debug(buyMessage)

    def sell(analysis):
        nonlocal sellMessage
        logging.debug(sellMessage)

    def latest_order_epoc_fn():
        return latest_order_epoc

    return default_kraken_strategy(**{"buy_fn":
                                      buy,
                                      "sell_fn":
                                      sell,
                                      "latest_order_epoc_fn":
                                      latest_order_epoc_fn},
                                   window_size=window_size)
