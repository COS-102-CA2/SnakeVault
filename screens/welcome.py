import tkinter as tk

from libs.window_manager import BG, FONT, FONT_DISPLAY, FONT_LG, GOLD, ICON_KEY, ICON_LOCK, ICON_SNAKE, MUTED, SURFACE2, TEXT, make_button


class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        content = tk.Frame(self, bg=BG)
        content.grid(row=0, column=0)

        tk.Label(content, text=f"{ICON_SNAKE}  {ICON_LOCK}", font=("Segoe UI Emoji", 42), fg=GOLD, bg=BG).pack(pady=(0, 24))
        tk.Label(content, text="SnakeVault", font=FONT_DISPLAY, fg=GOLD, bg=BG).pack()
        tk.Label(content, text="Your secure password manager", font=FONT, fg=MUTED, bg=BG).pack(pady=(8, 54))

        actions = tk.Frame(content, bg=BG)
        actions.pack()

        make_button(actions, f"{ICON_KEY} Create new vault", lambda: controller.show_screen("login"), font=FONT_LG).pack(
            side="left", padx=10, ipadx=22, ipady=10
        )
        make_button(actions, f"{ICON_LOCK} Unlock existing vault", lambda: controller.show_screen("login"), variant="secondary", font=FONT_LG).pack(
            side="left", padx=10, ipadx=22, ipady=10
        )

        tk.Label(content, text="AES encrypted · Zero knowledge · On-device master key", font=FONT, fg=MUTED, bg=BG).pack(pady=(36, 0))