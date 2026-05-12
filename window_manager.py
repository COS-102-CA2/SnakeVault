from setup import *
from helpers import *
frames:list[tk.Frame]=[]

def create_frame(root:tk.Tk):
    frame=tk.Frame(root)
    frames.append(frame)
    return frame

def show_frame(f:tk.Frame):
    for i in frames:
        i.pack_forget()
    f.pack()

class Screen:
    def __init__(self):
        self.frame=tk.Frame(root)
        frames.append(self.frame)
    def show(self):
        show_frame(self.frame)