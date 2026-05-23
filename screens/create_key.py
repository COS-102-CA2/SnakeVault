import tkinter as tk
from tkinter import messagebox

from libs.window_manager import BG, BORDER, DANGER, FONT, FONT_LG, FONT_TITLE, GOLD, ICON_KEY, MUTED, PAD_X, SURFACE, SURFACE2, TEXT, make_button, make_card, make_entry, make_field_label


class CreateKeyScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.show_key = False
        self.columnconfigure(0, weight=1)

        tk.Label(self, text=f"{ICON_KEY} Create Your Master Key", font=FONT_TITLE, fg=GOLD, bg=BG).grid(row=0, column=0, pady=(54, 8))
        tk.Label(self, text="This key encrypts everything in your vault", font=FONT, fg=MUTED, bg=BG).grid(row=1, column=0)

        card = make_card(self)
        card.grid(row=2, column=0, sticky="ew", padx=PAD_X, pady=28)
        card.columnconfigure(0, weight=1)

        make_field_label(card, "Master key").grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 6))

        row = tk.Frame(card, bg=SURFACE)
        row.grid(row=1, column=0, sticky="ew", padx=18)
        row.columnconfigure(0, weight=1)

        self.key_entry = make_entry(row, show="*")
        self.key_entry.grid(row=0, column=0, sticky="ew", ipady=8)
        self.key_entry.bind("<KeyRelease>", self.update_strength)

        self.toggle_btn = make_button(row, "Show", self.toggle_visibility, variant="secondary")
        self.toggle_btn.grid(row=0, column=1, padx=(8, 0), ipadx=12, ipady=7)

        self.strength_bar = tk.Frame(card, bg=BORDER, height=6)
        self.strength_bar.grid(row=2, column=0, sticky="ew", padx=18, pady=(12, 0))

        self.strength_fill = tk.Frame(self.strength_bar, bg=GOLD, width=0, height=6)
        self.strength_fill.place(x=0, y=0, relheight=1)

        self.strength_label = tk.Label(card, text="Minimum 8 characters", font=FONT, fg=MUTED, bg=SURFACE, anchor="w")
        self.strength_label.grid(row=3, column=0, sticky="ew", padx=18, pady=(8, 16))

        tk.Label(card, text="Use several words, numbers, or symbols.", font=FONT, fg=MUTED, bg=SURFACE, anchor="w").grid(
            row=4, column=0, sticky="ew", padx=18, pady=(0, 18)
        )

        tk.Label(self, text="If you lose this key your vault cannot be recovered.", font=FONT, fg=DANGER, bg=BG).grid(row=3, column=0)

        actions = tk.Frame(self, bg=BG)
        actions.grid(row=4, column=0, sticky="e", padx=PAD_X, pady=(28, 0))

        make_button(actions, "Cancel", self.cancel, variant="secondary").pack(side="right", ipadx=24, ipady=9)
        make_button(actions, "Continue →", self.continue_to_confirm, font=FONT_LG).pack(side="right", padx=(0, 12), ipadx=26, ipady=9)

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
            messagebox.showwarning("Master key too short", "Use at least 8 characters for your master key.")
            return
        self.controller.show_screen("confirm_key", master_key=key)

    def cancel(self):
        self.controller.master_key = None
        self.controller.show_screen("login")