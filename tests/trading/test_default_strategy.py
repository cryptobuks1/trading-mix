
from strategy_helper import bindings_for_default_kraken_strategy
import pytest
import logging


@pytest.mark.default_strategy
def test_default_strategy(ohlc_12_hour_as_sql, caplog):
    [strategy,
     events] = bindings_for_default_kraken_strategy(1534104841.0428, 3600 * 4)
    with caplog.at_level(logging.DEBUG):
        strategy(ohlc_12_hour_as_sql)

    assert "buy ~~~" in caplog.text
    assert "sell ~~~" not in caplog.text
