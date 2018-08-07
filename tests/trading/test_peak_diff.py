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


def collectPeak(peaks, results, data):
    peaks.append((data['result']['xpeak'][0],
                  data['result']['ypeak'][0]))
    results.append(data['result'])


@pytest.mark.peakdiff
def test_peak_diff(all_data):
    latest_order_epoc = {'epoc': 0}
    speaks = []

    def update_order_epoc(latest_order_epoc, peak_analysis):
        latest_order_epoc['epoc'] = peak_analysis['xpeak']

    engine, events = create(lambda: latest_order_epoc['epoc'],
                            tradeCommands)
    peaks = []
    results = []
    bind(events.foundPeak, partial(collectPeak, peaks, results))
    bind(events.newPeak, partial(update_order_epoc, latest_order_epoc))
    bind(events.newPeak,
         lambda peak_analysis: speaks.append((peak_analysis['xpeak'][0],
                                              peak_analysis['ypeak'][0])))
    for window in window_generator(3600 * 3,
                                   600,
                                   **{**all_data,
                                      **{'time_column': 'timestamp'}}):
        engine(window)
        if(len(peaks) == 100):
            break

    curpeak = None
    peakdiff = []
    for peak in [p[0] for p in speaks]:
        if not curpeak:
            curpeak = peak
        else:
            peakdiff.append(abs(peak - curpeak))
    assert 8620.408163309097 == min(peakdiff)
