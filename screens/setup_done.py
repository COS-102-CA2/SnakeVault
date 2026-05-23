import tkinter as tk

from libs.window_manager import BG, FONT, FONT_LG, FONT_TITLE, GOLD, ICON_LOCK, MUTED, SUCCESS, TEXT, make_button


class SetupDoneScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        content = tk.Frame(self, bg=BG)
        content.grid(row=0, column=0)

        tk.Label(content, text=ICON_LOCK, font=("Segoe UI Emoji", 46), fg=GOLD, bg=BG).pack(pady=(0, 22))
        tk.Label(content, text="Vault Setup Complete", font=FONT_TITLE, fg=GOLD, bg=BG).pack()
        tk.Label(content, text="Your master key is ready for this session.", font=FONT, fg=MUTED, bg=BG).pack(pady=(8, 10))
        tk.Label(content, text="Keep it somewhere safe offline.", font=FONT, fg=SUCCESS, bg=BG).pack(pady=(0, 42))

        make_button(content, "Enter dashboard", lambda: controller.show_screen("dashboard"), font=FONT_LG).pack(ipadx=44, ipady=10)
        make_button(content, "Back to sign in", lambda: controller.show_screen("login"), variant="secondary").pack(pady=14, ipadx=34, ipady=8)