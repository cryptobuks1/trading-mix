from trading.strategy.simple import create
from eventhelpers import update_order_with_peak
from trading.events import bind


def take(count, tradeCommands, gen):
    latest_order_epoc = {'epoc': 0}
    speaks = []

    engine, events = create(lambda: latest_order_epoc['epoc'],
                            tradeCommands)
    update_order_with_peak(events, latest_order_epoc)
    bind(events.newPeak,
         lambda peak_analysis: speaks.append(peak_analysis['xpeak'][0]))
    for window in (w if len(speaks) < count
                   else (_ for _ in ()).throw(StopIteration())
                   for w in gen):
        engine(window)
