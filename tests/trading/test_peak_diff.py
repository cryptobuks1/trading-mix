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


@pytest.mark.peakdiff
def test_peak_diff(all_data):
    latest_order_epoc = {'epoc': 0}
    speaks = []

    def update_order_epoc(latest_order_epoc, peak_analysis):
        latest_order_epoc['epoc'] = peak_analysis['xpeak']

    engine, events = create(lambda: latest_order_epoc['epoc'],
                            tradeCommands)
    results = []
    bind(events.newPeak, partial(update_order_epoc, latest_order_epoc))
    bind(events.newPeak,
         lambda peak_analysis: speaks.append(peak_analysis['xpeak'][0]))

    for window in  window_generator(3600 * 3,
                                                600,
                                                **all_data):
        engine(window)
        if len(speaks) == 20:
            break

    curpeak = None
    peakdiff = []
    for peak in speaks:
        if not curpeak:
            curpeak = peak
        else:
            peakdiff.append(abs(peak - curpeak))
    assert 8620.408163309097 == min(peakdiff)
