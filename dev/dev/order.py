from collections import namedtuple
from trading.events import bind


def simulation():
    Simulation = namedtuple("Simulation", ['trade_on_peak',
                                           'get_latest_order_epoc'])
    latest_order_epoc = 0

    def trade_on_peak(newPeakEvent):
        bind(newPeakEvent, update_latest_order_epoc)

    def update_latest_order_epoc(peak_analysis):
        nonlocal latest_order_epoc
        latest_order_epoc = peak_analysis['x'][0]

    def get_latest_order_epoc():
        return latest_order_epoc

    return Simulation(trade_on_peak,
                      get_latest_order_epoc)
