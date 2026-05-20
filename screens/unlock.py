import tkinter as tk
from tkinter import messagebox

from db import get_master_key
from libs.crypto import verify_key
from libs.window_manager import BG, BORDER, DANGER, GOLD, MUTED, SURFACE, SURFACE2, TEXT, FONT, FONT_LG, FONT_TITLE


class UnlockScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        tk.Label(
            self,
            text="Welcome Back",
            font=FONT_TITLE,
            fg=GOLD,
            bg=BG,
        ).pack(pady=(102, 8))

        tk.Label(
            self,
            text="Enter your master key to unlock your vault",
            font=FONT,
            fg=MUTED,
            bg=BG,
        ).pack()

        card = tk.Frame(
            self,
            bg=SURFACE,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        card.pack(fill="x", padx=108, pady=28, ipady=18)

        inner = tk.Frame(card, bg=SURFACE)
        inner.pack(fill="x", padx=18)

        tk.Label(
            inner,
            text="Master key",
            font=FONT,
            fg=MUTED,
            bg=SURFACE,
            anchor="w",
        ).pack(fill="x")

        self.key_entry = tk.Entry(
            inner,
            font=FONT,
            bg=SURFACE2,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            show="*",
        )
        self.key_entry.pack(fill="x", pady=(6, 12), ipady=8)
        self.key_entry.bind("<Return>", lambda _event: self.unlock())

        self.error_label = tk.Label(
            inner,
            text="",
            font=FONT,
            fg=DANGER,
            bg=SURFACE,
            anchor="w",
        )
        self.error_label.pack(fill="x")

        actions = tk.Frame(self, bg=BG)
        actions.pack()

        tk.Button(
            actions,
            text="Exit",
            font=FONT,
            bg=SURFACE2,
            fg=TEXT,
            bd=0,
            command=self.exit_to_login,
        ).pack(side="left", padx=8, ipadx=24, ipady=9)

        tk.Button(
            actions,
            text="Unlock vault",
            font=FONT_LG,
            bg=GOLD,
            fg="#161622",
            bd=0,
            command=self.unlock,
        ).pack(side="left", padx=8, ipadx=28, ipady=9)

        self.key_entry.focus_set()

    def unlock(self):
        entered_key = self.key_entry.get()

        if not entered_key:
            self.error_label.configure(text="Enter your master key.")
            return

        result = get_master_key()

        if not result["success"]:
            messagebox.showerror(
                "Unlock failed",
                result.get("error", "Could not check your master key."),
            )
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
            self.error_label.configure(
                text="Incorrect master key. Please try again."
            )

    def exit_to_login(self):
        self.controller.master_key = None
        self.controller.show_screen("login")