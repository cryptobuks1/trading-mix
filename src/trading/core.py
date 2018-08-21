
from trading.sql import time_range, window
from trading.strategy.simple import create
from enum import Enum


class TradeCommand(Enum):
    sell = 1
    buy = 2
    wait = 3


def default_kraken_strategy(*, buy_fn, sell_fn, latest_order_epoc_fn):
    tradeCommands = {
        TradeCommand.sell: sell_fn,
        TradeCommand.buy: buy_fn
    }

    engine, events = create(latest_order_epoc_fn, tradeCommands)

    def strategy(db):
        start, end = time_range(**db)
        engine(window(None,
                      end - 3600 * 4,
                      end, **db))

    return strategy, events
