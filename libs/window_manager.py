import tkinter as tk
from libs.common import *

frames: list[tk.Frame] = []

def show_frame(f: tk.Frame):
    for frame in frames:
        frame.pack_forget()
    f.pack(fill="both", expand=True)

class Screen:
    def __init__(self):
        self.root = root
        self.frame = tk.Frame(root)
        frames.append(self.frame)

    def show(self):
        show_frame(self.frame)