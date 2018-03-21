import pytest
from trading.data import fit, extract, peaks
from trading.util import toDate
from trading.ohlc import load
import trading.ohlc as oc
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


def ohlc(path):
    from trading.ohlc import readjsonfile
    return [record for record in readjsonfile(path)]

def ohlc_1513226220():
    from trading.ohlc import readjsonfile
    return [record for record in readjsonfile("/home/kristian/projects/kraken-bash/ohlc-1513226220.json")]


def ohlc_1513269300():
    from trading.ohlc import readjsonfile
    return [record for record in readjsonfile("/home/kristian/projects/kraken-bash/ohlc-1513269300.json")]


def ohlc_1516217100():
    return ohlc("/home/kristian/projects/kraken-bash/ohlc-1516217100.json")


def ohlc_1516320660():
    return ohlc("/home/kristian/projects/kraken-bash/ohlc-1516320660.json")

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
    offset = 0
    step = 600
    start = 1
    end = 2
    x, y = extract(data)
    plt.plot(x, y)
    while start + offset < end:
        start = 1513226220 + offset
        end = start + (3 * 3600)
        window = filter(lambda p: start <= p[0] <= end, data)
        _, _, xfit, yfit = fit(extract(window))
        p = peaks(yfit)
        print p

        if p:
            span = (xfit[-1] - xfit[p[0]]) / 60
            print span
            if 30 < span < 50:
                plt.plot(xfit, yfit, xfit[p], yfit[p], 'b+')
                print "### PEAK ###"
                print xfit[p[0]]
                print xfit[-1]
                print (xfit[-1] - xfit[p[0]]) / 60
        offset += step
    plt.show()


def test_ohlc_1513226220():
    print toDate(ohlc_1513226220()[-1][0])


def test_ohlc_1513269300():
    print toDate(ohlc_1513269300()[0][0])

def test_ohlc_1516217100():
    print toDate(ohlc_1516217100()[-1][0])


def test_ohlc_1516320660():
    print toDate(ohlc_1516320660()[0][0])

def test_combined_data():
    part1 = load("/home/kristian/projects/kraken-bash/ohlc-1521494568.json")
    part2 = load("/home/kristian/projects/kraken-bash/ohlc-1521533661.json")
    date = oc.join([part1, part2])

def test_date():
    print toDate(1521533580)
