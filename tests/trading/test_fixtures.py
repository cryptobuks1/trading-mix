import pytest
from os import getcwd
from os.path import join
import pickle
from trading.data import analyseData
from trading.octave import conf as peakConf
from trading.misc import desctructDict


def load_peak(path):
    with open(path, 'rb') as f:
        lp = pickle.load(f)
    return lp


@pytest.fixture
def low_peak():
    path = join(getcwd(), 'data', 'low_pickle.byte')
    return load_peak(path)


@pytest.fixture
def high_peak():
    path = join(getcwd(), 'data', 'high_pickle.byte')
    return load_peak(path)


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
