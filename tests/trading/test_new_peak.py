from trading.octave import conf as peakConf
from trading.events import tradingEvents
from trading.events import bind
from trading.data import analyseData
#from trading.core import advice
#from trading.core import TradeCommand
import pytest
#from functools import partial


def check_peak(latest_order_epoc, data):
    print("Got Peak")
    peakEpoc = data['result']['xpeak'][0]
    timeDiff = abs(peakEpoc - latest_order_epoc)
    if timeDiff < 1200:  # within 20 minutes
        tradingEvents.newPeak.send(check_peak, peak_analysis=data['result'])


def create_order(peak_analysis):
    assert False


@pytest.mark.newpeak
def test_new_peak(high_peak, high_peak_order_epoc):
    def onPeak(**kwargs):
        check_peak(high_peak_order_epoc, **kwargs)

    bind(tradingEvents.foundPeak, onPeak)
    bind(tradingEvents.newPeak, create_order)
    analyseData(peakConf, high_peak['data'],
                foundPeakEvent=tradingEvents.foundPeak)
