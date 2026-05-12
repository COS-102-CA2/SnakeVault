from setup import *
from window_manager import *

test_passwords=["boo","baa"]

class PasswordsScreen(Screen):
    def __init__(self):
        Screen.__init__(self)

        insertString(self.frame,"SnakeVault\n\n",("Inter",20))
        insertString(self.frame,"Passwords",("Inter",17))
        resultText=tk.Label(self.frame,text="")

        for i in test_passwords:
            insertString(self.frame,i,("Inter",17))
        tbox=tk.Entry(self.frame)
        
        
        tbox.pack(pady=(20,10))
        
        resultText.pack(pady=(20,10))