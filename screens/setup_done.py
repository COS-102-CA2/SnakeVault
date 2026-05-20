import tkinter as tk

from libs.window_manager import BG, GOLD, MUTED, SUCCESS, SURFACE2, TEXT, FONT, FONT_LG, FONT_TITLE


class SetupDoneScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        tk.Label(
            self,
            text="Vault Setup Complete",
            font=FONT_TITLE,
            fg=GOLD,
            bg=BG,
        ).pack(pady=(118, 8))

        tk.Label(
            self,
            text="Your master key is ready for this session.",
            font=FONT,
            fg=MUTED,
            bg=BG,
        ).pack()

        tk.Label(
            self,
            text="Keep it somewhere safe offline.",
            font=FONT,
            fg=SUCCESS,
            bg=BG,
        ).pack(pady=(18, 42))

        tk.Button(
            self,
            text="Enter dashboard",
            font=FONT_LG,
            bg=GOLD,
            fg="#161622",
            activebackground="#D8BA5C",
            bd=0,
            command=lambda: controller.show_screen("dashboard"),
        ).pack(ipadx=44, ipady=10)

        tk.Button(
            self,
            text="Back to sign in",
            font=FONT,
            bg=SURFACE2,
            fg=TEXT,
            bd=0,
            command=lambda: controller.show_screen("login"),
        ).pack(pady=14, ipadx=34, ipady=8)