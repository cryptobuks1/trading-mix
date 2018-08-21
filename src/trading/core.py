
from trading.sql import time_range, window
from trading.strategy.simple import create
from trading.data import TradeCommand
from enum import Enum
from collections import namedtuple


TradeActions = namedtuple('TradeActions', ["buy", "sell", "wait"])


def default_kraken_strategy(*, buy_fn, sell_fn, latest_order_epoc_fn):
    global TradeActions
    tradeCommands = {
        TradeCommand.sell: sell_fn,
        TradeCommand.buy: buy_fn
    }

    engine, events = create(latest_order_epoc_fn, tradeCommands)

    def strategy(db):
        nonlocal engine
        start, end = time_range(**db)
        engine(window(None,
                      end - 3600 * 3,
                      end, **db))

    return strategy, events
