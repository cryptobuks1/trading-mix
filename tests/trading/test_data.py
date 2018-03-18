import pytest
from trading.data import fit, extract, peaks
import matplotlib.pyplot as plt

@pytest.mark.fit
def test_fit():
    from trading.ohlc import readjsonfile
    ohlc_1513226220 = [record for record in readjsonfile("/home/kristian/projects/kraken-bash/ohlc-1513226220.json")]
    xidx = 0
    yidx = 1
    x, y, x_fit, y_fit = fit(extract(ohlc_1513226220, xidx, yidx))
    peaks_fit = peaks(y_fit)
    assert(len(x) == len(y))
    plt.plot(x, y, x_fit, y_fit, x_fit[peaks_fit], y_fit[peaks_fit], '+')
    plt.show()
    assert True


def ohlc_1513226220():
    from trading.ohlc import readjsonfile
    return [record for record in readjsonfile("/home/kristian/projects/kraken-bash/ohlc-1513226220.json")]

@pytest.mark.range
def test_range():
    three_hours = extract(filter(lambda p: 1513226220 <= p[0] > (1513226220 + (3 * 3600)), ohlc_1513226220()))

    [x, y] = extract(ohlc_1513226220)
    assert(len(x) == len(y))
    [subx, suby] = first_hour
    assert(len(subx) == len(suby))
    plt.plot(x, y, subx, suby)
    plt.show()
    assert True


def test_sub_fit():
    fit(extract(filter(lambda p: 1513226220 <= p[0] > (1513226220 + (3 * 3600)), ohlc_1513226220())))


def test_full_fit():
    import numpy as np
    #data = extract(ohlc_1513226220())
    data = extract(filter(lambda p: 1513226220 <= p[0] > (1513226220 + (3 * 3600)), ohlc_1513226220()))
    x, y, xfit, yfit = fit(data)
    print peaks(yfit)


def test_sliding_window():
    data = ohlc_1513226220()
    start = 1513226220
    end = (start + (3 * 3600))
    window = filter(lambda p: start <= p[0] > end, data)
    x, y, xfit, yfit = fit(extract(window))
    p = peaks(yfit)
    if p:
        plt.plot(x, y, xfit, yfit, xfit[p], yfit[p], '+')
