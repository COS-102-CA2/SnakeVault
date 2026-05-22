import tkinter as tk
from tkinter import messagebox

from libs.db import save_master_key
from libs.crypto import hash_key
from libs.window_manager import BG, BORDER, DANGER, GOLD, MUTED, SUCCESS, SURFACE, SURFACE2, TEXT, FONT, FONT_LG, FONT_TITLE


class ConfirmKeyScreen(tk.Frame):
    def __init__(self, parent, controller, master_key):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.master_key = master_key

        tk.Label(
            self,
            text="Confirm Your Master Key",
            font=FONT_TITLE,
            fg=GOLD,
            bg=BG,
        ).pack(pady=(72, 8))

        tk.Label(
            self,
            text="Re-enter your passphrase exactly",
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
        card.pack(fill="x", padx=54, pady=28, ipady=18)

        inner = tk.Frame(card, bg=SURFACE)
        inner.pack(fill="x", padx=18)

        tk.Label(
            inner,
            text="Master key again",
            font=FONT,
            fg=MUTED,
            bg=SURFACE,
            anchor="w",
        ).pack(fill="x")

        self.confirm_entry = tk.Entry(
            inner,
            font=FONT,
            bg=SURFACE2,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            show="*",
        )
        self.confirm_entry.pack(fill="x", pady=(6, 12), ipady=8)
        self.confirm_entry.bind("<KeyRelease>", self.update_match_state)

        self.match_label = tk.Label(
            inner,
            text="",
            font=FONT,
            fg=MUTED,
            bg=SURFACE,
            anchor="w",
        )
        self.match_label.pack(fill="x", ipady=8)

        actions = tk.Frame(self, bg=BG)
        actions.pack(fill="x", padx=54, pady=(86, 0))

        tk.Button(
            actions,
            text="Create vault",
            font=FONT_LG,
            bg=GOLD,
            fg="#161622",
            bd=0,
            command=self.create_vault,
        ).pack(side="right", ipadx=26, ipady=9)

        tk.Button(
            actions,
            text="Cancel",
            font=FONT,
            bg=SURFACE2,
            fg=TEXT,
            bd=0,
            command=self.cancel,
        ).pack(side="right", padx=(0, 12), ipadx=24, ipady=9)

        tk.Button(
            actions,
            text="Back",
            font=FONT,
            bg=SURFACE2,
            fg=TEXT,
            bd=0,
            command=self.go_back,
        ).pack(side="right", padx=(0, 12), ipadx=24, ipady=9)

        self.confirm_entry.focus_set()

    def update_match_state(self, _event=None):
        value = self.confirm_entry.get()

        if not value:
            self.match_label.configure(text="", fg=MUTED)
        elif value == self.master_key:
            self.match_label.configure(text="Keys match.", fg=SUCCESS)
        else:
            self.match_label.configure(text="Keys do not match.", fg=DANGER)

    def create_vault(self):
        if self.confirm_entry.get() != self.master_key:
            messagebox.showwarning(
                "Keys do not match",
                "Re-enter the same master key to continue.",
            )
            self.confirm_entry.delete(0, tk.END)
            self.update_match_state()
            return

        key_hash = hash_key(self.master_key)
        result = save_master_key(key_hash)

        if not result["success"]:
            messagebox.showerror(
                "Could not save master key",
                result.get("error", "Please try again."),
            )
            return

        self.controller.master_key = self.master_key
        self.master_key = None
        self.controller.show_screen("setup_done")

    def go_back(self):
        self.controller.show_screen("create_key")

    def cancel(self):
        self.master_key = None
        self.controller.master_key = None
        self.controller.show_screen("login")