from trading.ui import create_gui_window, update_ui, place_button
from trading.data import pause_frame_generator
from functools import partial


def control_graph(**kwargs):
    ui_window = create_gui_window()

    play_pause_state = {'continue': True}

    play_pause_graph_generator = partial(pause_frame_generator,
                                         play_pause_state)

    def play_pause_handler():
        nonlocal play_pause_state
        play_pause_state['continue'] = not play_pause_state['continue']

    place_button("Play/Pause", ui_window, play_pause_handler)
    update_ui(ui_window)
    return play_pause_graph_generator, ui_window
