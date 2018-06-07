from oct2py import octave
octave.eval("pkg load signal")


def transform(i):
    return int(i)


def peaks(values):
    ps = octave.findpeaks(values,
                          'DoubleSided',
                          'MinPeakHeight', 0.04,
                          'MinPeakDistance', 30,
                          'MinPeakWidth', 0, nout=3)
    if ps[1] and not isinstance(ps[1], list):
        ps = [[ps[0]], [ps[1]]]
    ps[1] = list(map(transform, ps[1]))
    return ps


conf = {"fn": peaks,
        "valuePos": 0,
        "indexPos": 1}
