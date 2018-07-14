import pytest
from os import getcwd
from os.path import join
from trading.data import load_data_from_file


@pytest.fixture
def low_peak():
    path = join(getcwd(), 'data', 'low_pickle.byte')
    return load_data_from_file(path)


@pytest.fixture
def high_peak():
    path = join(getcwd(), 'data', 'high_pickle.byte')
    return load_data_from_file(path)
