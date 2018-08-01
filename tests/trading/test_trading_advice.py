import pytest
from trading.data import analyseData
from trading.events import tradingEvents
from trading.octave import conf as peakConf
from trading.core import advice, TradeCommand


def validate_peak(peak_data, expected_advice):

    def onPeak(sender, data):
        assert advice(data['result']) == expected_advice

    event = tradingEvents.foundPeak
    event.connect(onPeak)
    analyseData(peakConf, peak_data)


@pytest.mark.regression
@pytest.mark.trading
def test_trading_low(low_peak):
    validate_peak(low_peak['data'], TradeCommand.buy)


@pytest.mark.regression
@pytest.mark.trading
def test_trading_high(high_peak):
    validate_peak(high_peak['data'], TradeCommand.sell)
