def pause_frame_generator(state, generator):
    for frame in generator:
        if state['continue']:
            print("Continue")
            yield frame
        else:
            while not state['continue']:
                yield frame
