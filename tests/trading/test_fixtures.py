import pytest
from trading.data import analyseData
from trading.octave import conf as peakConf
from trading.misc import desctructDict


@pytest.mark.fixture
def test_low_peak(low_peak):
    result = analyseData(peakConf, low_peak['data'])
    xpeak, z = desctructDict(result, ('xpeak', 'z'))
    assert z[0][1] < 0


@pytest.mark.fixture
def test_high_peak(high_peak):
    result = analyseData(peakConf, high_peak['data'])
    xpeak, z = desctructDict(result, ('xpeak', 'z'))
    assert z[0][1] > 0
