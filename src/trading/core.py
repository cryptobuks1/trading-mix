from trading.sql import time_range, window
from trading.strategy.simple import create
from trading.data import TradeCommand, extract, pause_frame_generator
from trading.events import TradingEvents, emit
from trading.plot import plot_data_with_x_as_date
from trading.ui import create_gui_window, update_ui, place_button
from collections import namedtuple
from functools import partial
import time


TradeActions = namedtuple('TradeActions', ["buy", "sell", "wait"])


def default_kraken_strategy(*,
                            buy_fn,
                            sell_fn,
                            latest_order_epoc_fn,
                            window_size=3600 * 5):
    ''' TODO Rename to default strategy
    '''
    global TradeActions
    tradeCommands = {
        TradeCommand.sell: sell_fn,
        TradeCommand.buy: buy_fn
    }

    engine, events = create(latest_order_epoc_fn, tradeCommands)

    def strategy(db, **kwargs):
        nonlocal engine
        start, end = time_range(**db)
        direction = kwargs.get("direction", "tail")
        offset = kwargs.get("offset", 0)
        if direction == "tail":
            window_start = end - offset - window_size
        elif direction == "head":
            window_start = start + offset

        window_end = window_start + window_size
        data = window(None,
                      window_start,
                      window_end, **db)
        emit(TradingEvents.data.fget(events), {"data": data})
        engine(data)


    return strategy, events


def control_graph(**kwargs):
    ui_window = create_gui_window()

    play_pause_state = {'continue': True}

    play_pause_graph_generator = partial(pause_frame_generator,
                                         play_pause_state)

    def play_pause_handler():
        nonlocal play_pause_state
        play_pause_state['continue'] = not play_pause_state['continue']

    def pause_graph():
        nonlocal play_pause_state
        play_pause_state['continue'] = False

    def is_paused_p():
        nonlocal play_pause_state
        return not play_pause_state['continue']

    place_button("Play/Pause", ui_window, play_pause_handler)
    return (play_pause_graph_generator,
            ui_window,
            play_pause_handler,
            pause_graph,
            is_paused_p)


def stream_data_to_graph(data_generator, events):
    (play_pause_graph_generator,
     window,
     play_pause_handler,
     pause_graph,
     is_paused_p) = control_graph()

    def run():
        for data in data_generator:
            update_ui(window)
            if not is_paused_p():
                emit(TradingEvents.data.fget(events), data=data)
            else:
                while is_paused_p():
                    time.sleep(0.3)
                    update_ui(window)
    return run, window, play_pause_handler, pause_graph
