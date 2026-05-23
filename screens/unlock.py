import tkinter as tk
from tkinter import messagebox

from libs.db import get_master_key
from libs.crypto import verify_key
from libs.window_manager import BG, BORDER, DANGER, FONT, FONT_LG, FONT_TITLE, GOLD, ICON_LOCK, MUTED, PAD_X, SURFACE, TEXT, make_button, make_card, make_entry, make_field_label


class UnlockScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.columnconfigure(0, weight=1)

        tk.Label(self, text=ICON_LOCK, font=("Segoe UI Emoji", 44), fg=GOLD, bg=BG).grid(row=0, column=0, pady=(76, 20))
        tk.Label(self, text="Welcome Back", font=FONT_TITLE, fg=GOLD, bg=BG).grid(row=1, column=0)
        tk.Label(self, text="Enter your master key to unlock your vault", font=FONT, fg=MUTED, bg=BG).grid(row=2, column=0, pady=(8, 24))

        card = make_card(self)
        card.grid(row=3, column=0, sticky="ew", padx=PAD_X * 2, pady=(0, 20))
        card.columnconfigure(0, weight=1)

        make_field_label(card, "Master key").grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 6))
        self.key_entry = make_entry(card, show="*")
        self.key_entry.grid(row=1, column=0, sticky="ew", padx=18, ipady=9)
        self.key_entry.bind("<Return>", lambda _event: self.unlock())

        self.error_label = tk.Label(card, text="", font=FONT, fg=DANGER, bg=SURFACE, anchor="w")
        self.error_label.grid(row=2, column=0, sticky="ew", padx=18, pady=(10, 18))

        actions = tk.Frame(self, bg=BG)
        actions.grid(row=4, column=0)

        make_button(actions, "Exit", self.exit_to_login, variant="secondary").pack(side="left", padx=8, ipadx=24, ipady=9)
        make_button(actions, f"{ICON_LOCK} Unlock vault", self.unlock, font=FONT_LG).pack(side="left", padx=8, ipadx=28, ipady=9)

        self.key_entry.focus_set()

    def unlock(self):
        entered_key = self.key_entry.get()
        if not entered_key:
            self.error_label.configure(text="Enter your master key.")
            return

        result = get_master_key()
        if not result["success"]:
            messagebox.showerror("Unlock failed", result.get("error", "Could not check your master key."))
            return

        stored_hash = result["data"]
        if not stored_hash:
            self.controller.show_screen("create_key")
            return

        if verify_key(entered_key, stored_hash):
            self.controller.master_key = entered_key
            self.key_entry.delete(0, tk.END)
            self.controller.show_screen("dashboard")
        else:
            self.key_entry.delete(0, tk.END)
            self.error_label.configure(text="Incorrect master key. Please try again.")

    def exit_to_login(self):
        self.controller.master_key = None
        self.controller.show_screen("login")