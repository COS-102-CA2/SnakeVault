import customtkinter as ctk
from tkinter import messagebox

from libs.window_manager import (
    BG,
    BORDER,
    DANGER,
    FONT,
    FONT_LG,
    FONT_TITLE,
    GOLD,
    ICON_KEY,
    MUTED,
    PAD_X,
    SUCCESS,
    SURFACE,
    make_button,
    make_card,
    make_entry,
    make_field_label,
)


class CreateKeyScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.controller = controller
        self.show_key = False

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            self,
            text=f"{ICON_KEY} Create Your Master Key",
            font=FONT_TITLE,
            text_color=GOLD,
        ).grid(row=0, column=0, pady=(44, 8))

        ctk.CTkLabel(
            self,
            text="This key encrypts everything in your vault",
            font=FONT,
            text_color=MUTED,
        ).grid(row=1, column=0)

        card = make_card(self)
        card.grid(row=2, column=0, sticky="nsew", padx=PAD_X, pady=24)
        card.grid_columnconfigure(0, weight=1)

        form = ctk.CTkFrame(card, fg_color=SURFACE, corner_radius=0)
        form.grid(row=0, column=0, sticky="nsew", padx=18, pady=18)
        form.grid_columnconfigure(0, weight=1)

        make_field_label(form, "Master key").grid(row=0, column=0, sticky="ew", pady=(0, 6))

        row = ctk.CTkFrame(form, fg_color=SURFACE, corner_radius=0)
        row.grid(row=1, column=0, sticky="ew")
        row.grid_columnconfigure(0, weight=1)

        self.key_entry = make_entry(row, show="*")
        self.key_entry.grid(row=0, column=0, sticky="ew", ipady=5)
        self.key_entry.bind("<KeyRelease>", self.update_strength)

        self.toggle_btn = make_button(
            row,
            "Show",
            self.toggle_visibility,
            variant="secondary",
        )
        self.toggle_btn.grid(row=0, column=1, padx=(8, 0), ipadx=12, ipady=5)

        meter = ctk.CTkFrame(form, fg_color=SURFACE, corner_radius=0)
        meter.grid(row=2, column=0, sticky="ew", pady=(12, 0))
        for index in range(4):
            meter.grid_columnconfigure(index, weight=1)

        self.meter_segments = []
        for index in range(4):
            segment = ctk.CTkFrame(meter, fg_color=BORDER, height=6, corner_radius=4)
            segment.grid(row=0, column=index, sticky="ew", padx=(0, 4))
            self.meter_segments.append(segment)

        self.strength_label = ctk.CTkLabel(
            form,
            text="Minimum 8 characters",
            font=FONT,
            text_color=MUTED,
            fg_color=SURFACE,
            anchor="w",
        )
        self.strength_label.grid(row=3, column=0, sticky="ew", pady=(8, 16))

        ctk.CTkLabel(
            form,
            text="Tips: use several words, mix numbers, and add symbols.",
            font=FONT,
            text_color=MUTED,
            fg_color=SURFACE,
            anchor="w",
        ).grid(row=4, column=0, sticky="ew", pady=(0, 8))

        ctk.CTkLabel(
            form,
            text="If you lose this key your vault cannot be recovered.",
            font=FONT,
            text_color=DANGER,
            fg_color=SURFACE,
            anchor="w",
        ).grid(row=5, column=0, sticky="ew")

        actions = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        actions.grid(row=3, column=0, sticky="e", padx=PAD_X, pady=(0, 24))

        make_button(actions, "Cancel", self.cancel, variant="secondary").pack(side="right", ipadx=18, ipady=6)
        make_button(actions, "Continue →", self.continue_to_confirm, font=FONT_LG).pack(side="right", padx=(0, 12), ipadx=20, ipady=6)

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
        colors = [DANGER, DANGER, "#D6A94F", GOLD, SUCCESS]

        for index, segment in enumerate(self.meter_segments):
            segment.configure(fg_color=colors[score] if index < score else BORDER)

        self.strength_label.configure(
            text=labels[score],
            text_color=colors[score],
        )

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