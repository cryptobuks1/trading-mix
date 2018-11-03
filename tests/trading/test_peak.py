from trading.events import (create_trading_events,
                            bind,
                            emit,
                            TradingEvents)
from trading.sql import sqlite_connect
from trading.data import (window_generator,
                          analyseData,
                          is_new_peak,
                          TradeCommand)
from trading.octave import conf as peakConf
from trading.strategy.simple import trigger_trade_advise
from os.path import join
from dev.order import simulation
from functools import partial
from collections import namedtuple
import logging
import pytest

@pytest.mark.peaks
@pytest.mark.parametrize("data_file, peaks", [
    ("ohcl-2018-08-21-22:22:09.sqlite",
     [(1534847494.2857144, TradeCommand.buy),
      (1534863939.1836734, TradeCommand.sell),
      (1534878412.6530612, TradeCommand.buy)])
])
def test_peaks(data_file, peaks, data_dir, caplog):
    result = []
    advices = []
    db = sqlite_connect(join(data_dir,
                             data_file))
    events = create_trading_events()
    analyse_using_octave = partial(analyseData,
                                   peakConf,
                                   foundPeakEvent=events.foundPeak)
    sim = simulation()
    sim.trade_on_peak(events.newPeak)
    bind(events.newPeak, partial(trigger_trade_advise, events))
    bind(events.newPeak,
         lambda peak_analysis: result.append(peak_analysis['xpeak'][0]))
    bind(events.foundPeak,
         lambda data: emit(events.newPeak,
                           data={
                               "peak_analysis":
                               data['result']},
                           unpack_data=True)
         if is_new_peak(sim.get_latest_order_epoc,
                        data['result'])
         else None)
    bind(events.advice,
         lambda data:
         logging.debug("~SELL~"
                       if data['advice'] == TradeCommand.sell
                       else "~BUY~"))
    with caplog.at_level(logging.DEBUG):
        for data in window_generator(3600 * 3,
                                     600,
                                     **db):
            analyse_using_octave(data)
        logging.debug(result)
        logging.debug(peaks)
    assert result == [peak_info[0] for peak_info in peaks]
    assert advices == [peak_info[1] for peak_info in peaks]
