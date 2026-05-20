put in create_key.py :
import tkinter as tk
from tkinter import messagebox

from libs.window_manager import BG, BORDER, DANGER, GOLD, MUTED, SURFACE, SURFACE2, TEXT, FONT, FONT_LG, FONT_TITLE


class CreateKeyScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.show_key = False

        tk.Label(
            self,
            text="Create Your Master Key",
            font=FONT_TITLE,
            fg=GOLD,
            bg=BG,
        ).pack(pady=(64, 8))

        tk.Label(
            self,
            text="This key encrypts everything in your vault",
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
            text="Master key",
            font=FONT,
            fg=MUTED,
            bg=SURFACE,
            anchor="w",
        ).pack(fill="x")

        row = tk.Frame(inner, bg=SURFACE)
        row.pack(fill="x", pady=(6, 10))

        self.key_entry = tk.Entry(
            row,
            font=FONT,
            bg=SURFACE2,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            show="*",
        )
        self.key_entry.pack(side="left", fill="x", expand=True, ipady=8)
        self.key_entry.bind("<KeyRelease>", self.update_strength)

        self.toggle_btn = tk.Button(
            row,
            text="Show",
            font=FONT,
            bg=SURFACE2,
            fg=TEXT,
            bd=0,
            command=self.toggle_visibility,
        )
        self.toggle_btn.pack(side="left", padx=(8, 0), ipady=7, ipadx=12)

        self.strength_bar = tk.Frame(inner, bg=BORDER, height=6)
        self.strength_bar.pack(fill="x")

        self.strength_fill = tk.Frame(
            self.strength_bar,
            bg=GOLD,
            width=0,
            height=6,
        )
        self.strength_fill.place(x=0, y=0, relheight=1)

        self.strength_label = tk.Label(
            inner,
            text="Minimum 8 characters",
            font=FONT,
            fg=MUTED,
            bg=SURFACE,
            anchor="w",
        )
        self.strength_label.pack(fill="x", pady=(8, 16))

        tk.Label(
            inner,
            text="Use a memorable passphrase with several words, numbers, or symbols.",
            font=FONT,
            fg=MUTED,
            bg=SURFACE,
            anchor="w",
        ).pack(fill="x")

        tk.Label(
            self,
            text="If you lose this key your vault cannot be recovered.",
            font=FONT,
            fg=DANGER,
            bg=BG,
        ).pack(pady=(10, 0))

        actions = tk.Frame(self, bg=BG)
        actions.pack(fill="x", padx=54, pady=(30, 0))

        tk.Button(
            actions,
            text="Cancel",
            font=FONT,
            bg=SURFACE2,
            fg=TEXT,
            bd=0,
            command=self.cancel,
        ).pack(side="right", ipadx=24, ipady=9)

        tk.Button(
            actions,
            text="Continue",
            font=FONT_LG,
            bg=GOLD,
            fg="#161622",
            bd=0,
            command=self.continue_to_confirm,
        ).pack(side="right", padx=(0, 12), ipadx=26, ipady=9)

        self.key_entry.focus_set()

    def toggle_visibility(self):
        self.show_key = not self.show_key
        self.key_entry.configure(show="" if self.show_key else "*")
        self.toggle_btn.configure(text="Hide" if self.show_key else "Show")

    def strength_score(self, value):
        score = 0

        if len(value) >= 8:
            score += 1
        if len(value) >= 12:
            score += 1
        if any(char.isdigit() for char in value):
            score += 1
        if any(not char.isalnum() for char in value):
            score += 1

        return score

    def update_strength(self, _event=None):
        key = self.key_entry.get()
        score = self.strength_score(key)

        labels = ["Too short", "Weak", "Fair", "Good", "Strong"]
        colors = [DANGER, DANGER, "#D6A94F", GOLD, "#75C878"]

        width = max(1, score) / 4
        self.strength_fill.place_configure(relwidth=width)
        self.strength_fill.configure(bg=colors[score])
        self.strength_label.configure(text=labels[score], fg=colors[score])

    def continue_to_confirm(self):
        key = self.key_entry.get()

        if len(key) < 8:
            messagebox.showwarning(
                "Master key too short",
                "Use at least 8 characters for your master key.",
            )
            return

        self.controller.show_screen("confirm_key", master_key=key)

    def cancel(self):
        self.controller.master_key = None
        self.controller.show_screen("login")