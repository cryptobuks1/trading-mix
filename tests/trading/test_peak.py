from trading.events import create_trading_events, bind
from trading.sql import sqlite_connect
from trading.data import (window_generator,
                          analyseData)
from trading.octave import conf as peakConf
from dev.order import simulation
from functools import partial
import logging
import pytest


@pytest.mark.peaks
@pytest.mark.parametrize("data_file, peaks", [
    ("ohcl-2018-08-21-22:22:09.sqlite", [1534863939.1836734,
                                         1534878412.6530612])
])
def test_peaks(data_file, peaks, caplog):
    db = sqlite_connect(data_file)
    events = create_trading_events()
    analyse_using_octave = partial(analyseData,
                                   peakConf,
                                   foundPeakEvent=events.foundPeak)
    sim = simulation()
    sim.trade_on_peak(events.newPeak)
    bind(events.foundPeak,
         lambda data: emit(events.newPeak,
                           data={
                               "peak_analysis":
                               data['result']},
                           unpack_data=True)
         if is_new_peak(get_latest_order_epoc,
                        data['result'])
         else None)
    with caplog.at_level(logging.DEBUG):
        for data in window_generator(3600 * 3,
                                     600,
                                     **db):
            analyse_using_octave(data)
