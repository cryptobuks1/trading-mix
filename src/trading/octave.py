from oct2py import octave
octave.eval("pkg load signal")


def transform(i):
    return int(i)


def peaks(values, **kwargs):
    if 'peak_params' in kwargs:
        peak_params = kwargs['peak_params']
    else:
        peak_params = ('DoubleSided',
                       'MinPeakHeight', 0.3,
                       'MinPeakDistance', 30,
                       'MinPeakWidth', 0)
    ps = octave.findpeaks(values,
                          *peak_params,
                          nout=3)
    if ps[1] and not isinstance(ps[1], list):
        ps = [[ps[0]], [ps[1]]]
    ps[1] = list(map(transform, ps[1]))
    return ps


conf = {"fn": peaks,
        "valuePos": 0,
        "indexPos": 1}
