import trading

def test_fit():
    from trading.ohlc import readjsonfile
    ohlc_1513226220 = [record for record in readjsonfile("/home/kristian/projects/kraken-bash/ohlc-1513226220.json")]
    xidx = 0
    yidx = 1
    [x, y, x_fit, y_fit, peaks_fit] = fit(extract(ohlc_1513226220, xidx, yidx))
    plt.plot(x, y, x_fit, y_fit, x_fit[peaks_fit], y_fit[peaks_fit], '+')
    plt.show()
