import tkinter as tk
def insertString(root:tk.T,s:str,font):
    lbl=tk.Label(root)
    lbl.configure(font=font,text=s)
    lbl.pack()