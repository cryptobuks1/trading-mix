import pytest
from os import getcwd
from os.path import join
import pickle


@pytest.fixture
def low_peak():
    path = join(getcwd(), 'data', 'low_pickle.byte')
    with open(path, 'rb') as f:
        return path


@pytest.mark.fixture
def test_low_peak(low_peak):
    assert '' == low_peak
