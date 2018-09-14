
from strategy_helper import bindings_for_default_kraken_strategy
from trading.events import TradingEvents, bind
from trading.kraken import ohlc
from trading.sql import connect
from os.path import expanduser, join
import os
from shutil import copyfile
import pytest
import tempfile
import logging


@pytest.mark.default_strategy_store
def test_default_strategy(caplog):
    def save_data(tmp_db_file):
        data_dir = expanduser('~/.local/lib/trading/data/orders')
        os.makedirs(data_dir)
        stored_date_file = join(data_dir, "date_data.sqlite")
        copyfile(tmp_db_file, stored_date_file)
        raise Exception("Hest")

    [strategy,
     events] = bindings_for_default_kraken_strategy(1534104841.0428, 3600 * 4)
    with caplog.at_level(logging.DEBUG):
        with tempfile.NamedTemporaryFile(prefix='pickle') as f:
            bind(TradingEvents.tradeAdvise.fget(events), save_data)
            db = connect('sqlite:///' + f.name)
            ohlc(**db)
            strategy(db)
    assert "buy ~~~" in caplog.text
