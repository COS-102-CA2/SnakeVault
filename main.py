from libs.window_manager import *
from screens.title import *
from libs.common import *

root=Tk()
root.geometry('600x400')
root.resizable(False,False)


w=TitleScreen()
w.show()


root.mainloop()