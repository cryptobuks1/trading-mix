from enum import Enum


class TradeCommand(Enum):
    sell = 1
    buy = 2
    wait = 3


def advice(analysis):
    z = analysis['z']
    if z[0][1] < 0:
        return TradeCommand.buy
    else:
        return TradeCommand.sell

def default_db_path():
