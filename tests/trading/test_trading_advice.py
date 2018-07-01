import pytest
from trading.data import foundPeakEvent, analyseData
from trading.octave import conf as peakConf
from trading.core import advice, TradeCommand
from blinker import signal


def validate_peak(peak_data, expected_advice):

    def onPeak(sender, data):
        assert advice(data['result']) == expected_advice

    event = signal(foundPeakEvent)
    event.connect(onPeak)
    analyseData(peakConf, peak_data)


@pytest.mark.trading
def test_trading_low(low_peak):
    validate_peak(low_peak['data'], TradeCommand.buy)


@pytest.mark.trading
def test_trading_high(high_peak):
    validate_peak(high_peak['data'], TradeCommand.sell)
