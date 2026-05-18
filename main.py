import tkinter as tk
from libs.window_manager import Screen
from screens.welcome import WelcomeScreen
from libs.common import *

# Create the one and only application window
root.title("SnakeVault")
root.geometry("600x400")
root.resizable(False, False)

# Show the first screen
welcome = WelcomeScreen()
welcome.show()

# Start the app — this line keeps the window open and listening for clicks
root.mainloop()