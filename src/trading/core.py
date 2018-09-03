
from trading.sql import time_range, window
from trading.strategy.simple import create
from trading.data import TradeCommand
from enum import Enum
from collections import namedtuple


TradeActions = namedtuple('TradeActions', ["buy", "sell", "wait"])


def default_kraken_strategy(*,
                            buy_fn,
                            sell_fn,
                            latest_order_epoc_fn,
                            window_size=3600 * 5):
    global TradeActions
    tradeCommands = {
        TradeCommand.sell: sell_fn,
        TradeCommand.buy: buy_fn
    }

    engine, events = create(latest_order_epoc_fn, tradeCommands)

    def strategy(db, **kwargs):
        nonlocal engine
        start, end = time_range(**db)
        direction = kwargs.get("direction", "tail")
        offset = kwargs.get("offset", 0)
        if direction == "tail":
            window_start = end - offset - window_size
        elif direction == "head":
            window_start = start + offset

        window_end = window_start + window_size
        engine(window(None,
                      window_start,
                      window_end, **db))

    return strategy, events
