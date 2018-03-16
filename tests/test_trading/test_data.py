import pytest
from trading.data import fit, extract
import matplotlib.pyplot as plt

def test_fit():
    from trading.ohlc import readjsonfile
    ohlc_1513226220 = [record for record in readjsonfile("/home/kristian/projects/kraken-bash/ohlc-1513226220.json")]
    xidx = 0
    yidx = 1
    [x, y, x_fit, y_fit, peaks_fit] = fit(extract(ohlc_1513226220, xidx, yidx))
    plt.plot(x, y, x_fit, y_fit, x_fit[peaks_fit], y_fit[peaks_fit], '+')
    plt.show()
    assert True

@pytest.mark.range
def test_range():
    from trading.ohlc import readjsonfile
    ohlc_1513226220 = [record for record in readjsonfile("/home/kristian/projects/kraken-bash/ohlc-1513226220.json")]
    first_hour = extract(filter(lambda p: 1513226220 <= p[0] > (1513226220 + (3 * 3600)), ohlc_1513226220))

    [x, y] = extract(ohlc_1513226220)
    [subx, suby] = first_hour
    plt.plot(x, y, subx, suby)
    plt.show()
    assert True
