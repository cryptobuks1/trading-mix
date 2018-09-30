from tkinter import Tk, Button


def show_control_window(play_pause_fn, recordEvent):
    top = Tk()
    top.geometry("150x100")

    def helloCallBack():
        play_pause_fn()

    def recordCallback():
        print("record")
        recordEvent.send('ui')

    B = Button(top, text="Hello", command=helloCallBack)
    B.place(x=50, y=0)
    RB = Button(top, text="Record", command=recordCallback)
    RB.place(x=50, y=50)
    top.mainloop()


def create_gui_window(**kwargs):
    window = Tk()
    width = kwargs.get("width", 300)
    height = kwargs.get("height", 200)
    window.geometry("{}x{}".format(width, height))
    return window


def update_ui(window):
    window.update_idletasks()
    window.update()


def place_button(label, destination, on_click_handler, **kwargs):
    button = Button(destination, text=label, command=on_click_handler).pack()
