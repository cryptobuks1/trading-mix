from trading.events import bind
from functools import partial


def update_order_with_peak(events, latest_order_epoc):
    bind(events.newPeak, partial(update_order_epoc, latest_order_epoc))


def update_order_epoc(latest_order_epoc, peak_analysis):
    latest_order_epoc['epoc'] = peak_analysis['x'][-1]
