import tkinter as tk

from libs.window_manager import BG, GOLD, MUTED, SURFACE2, TEXT, FONT, FONT_LG, FONT_TITLE


class WelcomeScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        tk.Label(
            self,
            text="SnakeVault",
            font=FONT_TITLE,
            fg=GOLD,
            bg=BG,
        ).pack(pady=(120, 8))

        tk.Label(
            self,
            text="Your secure password manager",
            font=FONT,
            fg=MUTED,
            bg=BG,
        ).pack(pady=(0, 50))

        tk.Button(
            self,
            text="Continue to login",
            font=FONT_LG,
            bg=GOLD,
            fg="#161622",
            activebackground="#D8BA5C",
            bd=0,
            command=lambda: controller.show_screen("login"),
        ).pack(ipadx=36, ipady=10)

        tk.Button(
            self,
            text="Exit",
            font=FONT,
            bg=SURFACE2,
            fg=TEXT,
            activebackground=SURFACE2,
            activeforeground=TEXT,
            bd=0,
            command=controller.destroy,
        ).pack(pady=14, ipadx=28, ipady=8)