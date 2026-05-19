import tkinter as tk

from screens.welcome import WelcomeScreen
from screens.login_screen import LoginScreen
from screens.create_key import CreateKeyScreen
from screens.confirm_key import ConfirmKeyScreen
from screens.setup_done import SetupDoneScreen
from screens.unlock import UnlockScreen
from screens.dashboard_screen import DashboardScreen
from screens.add_password import AddPasswordScreen
from screens.password_detail import PasswordDetailScreen
from screens.generator import GeneratorScreen
from screens.search import SearchScreen
from screens.settings import SettingsScreen


class SnakeVaultApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("SnakeVault - Password Manager")
        self.geometry("800x550")
        self.configure(bg="#1E1E2E")

        self.container = tk.Frame(self, bg="#1E1E2E")
        self.container.pack(fill="both", expand=True)

        self.current_screen = None
        self.master_key = None

        self.show_screen("welcome")

    def show_screen(self, screen_name, **kwargs):
        if self.current_screen is not None:
            self.current_screen.destroy()

        screens = {
            "welcome": lambda: WelcomeScreen(self.container, self),
            "login": lambda: LoginScreen(self.container, self),
            "create_key": lambda: CreateKeyScreen(self.container, self),
            "confirm_key": lambda: ConfirmKeyScreen(self.container, self, **kwargs),
            "setup_done": lambda: SetupDoneScreen(self.container, self),
            "unlock": lambda: UnlockScreen(self.container, self),
            "dashboard": lambda: DashboardScreen(self.container, self),
            "add_password": lambda: AddPasswordScreen(self.container, self),
            "password_detail": lambda: PasswordDetailScreen(self.container, self, **kwargs),
            "generator": lambda: GeneratorScreen(self.container, self),
            "search": lambda: SearchScreen(self.container, self),
            "settings": lambda: SettingsScreen(self.container, self),
        }

        if screen_name in screens:
            self.current_screen = screens[screen_name]()
            self.current_screen.pack(fill="both", expand=True)


if __name__ == "__main__":
    app = SnakeVaultApp()
    app.mainloop()