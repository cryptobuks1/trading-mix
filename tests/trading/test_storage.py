
import pytest
from trading.storage import save, load
import logging

@pytest.mark.storage
def test_storage(caplog):
    balance_in1 = {'euros': 1,
                   'xmr': 1}
    balance_in2 = {'euros': 2,
                   'xmr': 2}
    balance_in3 = {'euros': 3,
                   'xmr': 3}
    with caplog.at_level(logging.DEBUG):
        save('balance', balance_in1)
        save('balance', balance_in2)
        save('balance', balance_in3)
        balance_out = load('balance')
    assert balance_in3 == balance_out
