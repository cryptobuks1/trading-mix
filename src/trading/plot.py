import matplotlib.pyplot as plt
def axis_with_dates_x():
    fig, ax = plt.subplots()
    fig.autofmt_xdate()
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
    return fig, ax
