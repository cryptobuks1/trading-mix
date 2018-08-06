from trading.core import TradeCommand
from trading.strategy.simple import create
from trading.data import window_generator
from trading.events import bind
from functools import partial
import pytest
import logging


tradeCommands = {
    TradeCommand.sell: lambda: True,
    TradeCommand.buy: lambda: True
}


def collectPeak(peaks, data):
    peaks.append(data['result']['xpeak'][0])


@pytest.mark.peakdiff
def test_peak_diff(all_data):
    engine, events = create(0,
                            tradeCommands)
    peaks = []
    bind(events.foundPeak, partial(collectPeak, peaks))
    for window in window_generator(3600 * 3,
                                   600,
                                   **{**all_data,
                                      **{"time_column": "timestamp"}}):
        engine(window)
        if(len(peaks) == 100):
            break
    curpeak = None
    newpeaks = []
    for peak in peaks:
        if not curpeak or 1200 < abs(peak - curpeak):
            curpeak = peak
            newpeaks.append(curpeak)
    curpeak = None
    peakdiff = []
    for peak in newpeaks:
        if not curpeak:
            curpeak = peak
        else:
            peakdiff.append(abs(peak - curpeak))
    print(min(peakdiff))
    assert [] == newpeaks
