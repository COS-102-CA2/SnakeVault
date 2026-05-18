import tkinter as tk
from screens.login_screen import LoginScreen
from screens.dashboard_screen import DashboardScreen

class SnakeVaultApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("SnakeVault - Password Manager")
        self.geometry("800x550")
        self.configure(bg="#1e1e2e")  # Modern dark theme background
        
        # Container frame to hold different screens
        self.container = tk.Frame(self, bg="#1e1e2e")
        self.container.pack(fill="both", expand=True)

        # Track the active screen
        self.current_screen = None
        
        # Show login screen on startup
        self.show_screen("login")

    def show_screen(self, screen_name):
        """Destroys the current screen and loads the requested one."""
        if self.current_screen is not None:
            self.current_screen.destroy()

        if screen_name == "login":
            self.current_screen = LoginScreen(self.container, self)
        elif screen_name == "dashboard":
            self.current_screen = DashboardScreen(self.container, self)
            
        self.current_screen.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = SnakeVaultApp()
    app.mainloop()