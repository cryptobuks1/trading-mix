from trading.octave import conf as peakConf
from trading.events import tradingEvents, defaultEventBindings, bindEvents
from trading.data import analyseData
import pytest


@pytest.mark.newpeak
def test_new_peak(high_peak):

    def onPeak(sender, data):
        assert True

    reactions = defaultEventBindings._replace(foundPeak=onPeak)
    bindEvents(tradingEvents, reactions)

    analyseData(peakConf, high_peak['data'])
