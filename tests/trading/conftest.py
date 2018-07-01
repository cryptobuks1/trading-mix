import pytest
from os import getcwd
from os.path import join
import pickle


@pytest.fixture
def load_peak():
    def peak_loader(path):
        with open(path, 'rb') as f:
            lp = pickle.load(f)
            return lp
    return peak_loader


@pytest.fixture
def low_peak(load_peak):
    path = join(getcwd(), 'data', 'low_pickle.byte')
    return load_peak(path)


@pytest.fixture
def high_peak(load_peak):
    path = join(getcwd(), 'data', 'high_pickle.byte')
    return load_peak(path)
