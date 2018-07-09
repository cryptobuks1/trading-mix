from trading.octave import conf as peakConf
from trading.data import foundPeakEvent, analyseData
from trading.core import isNewPeak


def test_new_peak(high_peak):

    def onPeak(sender, peakEvent):
        isNewPeak(peakEvent)

    analyseData(peakConf, high_peak['data'])
