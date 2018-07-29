from trading.strategy.simple import run
from trading.core import TradeCommand
from trading.kraken import ohlc, get_orders
from trading.sql import memdb, meta, latest, time_range, window
from trading.mail import send, create_message
from toml import load
from os.path import expanduser
from functools import partial
import pytest
import logging


@pytest.mark.notify
def test_notify(high_peak, caplog):
    conf = load(expanduser('~/trading.toml'))

    def send_mail(message):
        send(message,
             conf['mail']['username'],
             conf['mail']['password'])

    db = memdb()
    tradeCommands = {
        TradeCommand.sell: partial(send_mail, make_message("Sell")),
        TradeCommand.buy: partial(send_mail, make_message("Buy"))
    }
    get_orders(**db)
    ohlc(**db)
    env = db.copy()
    env.update({'meta_data': meta(db['connection']),
                'table_name': 'orders'})
    latestOrder = latest(**env)
    start, end = time_range(**db)
    with caplog.at_level(logging.DEBUG):
        run(latestOrder.time, tradeCommands, high_peak['data'])
    assert "Found peak" in caplog.text


def make_message(advice):
    return create_message("kristian.n.jensen@gmail.com",
                          "kristian@freeduck.dk",
                          "Advice",
                          advice)
