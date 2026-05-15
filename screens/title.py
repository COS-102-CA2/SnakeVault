from setup import *
from libs.window_manager import *
from screens.dashboard import *




def password_click():
    print("Button pressed")
    PasswordsScreen().show()



class TitleScreen(Screen):
    def __init__(self):
        Screen.__init__(self)

        insertString(self.frame,"SnakeVault",("Inter",20))
        insertString(self.frame,"Enter the master password.",("Inter",10))
        resultText=tk.Label(self.frame,text="")


        tbox=tk.Entry(self.frame)
        btn=tk.Button(self.frame,text="Ok",command=password_click)
        
        tbox.pack(pady=(20,10))
        btn.pack(pady=(20,10))
        resultText.pack(pady=(20,10))