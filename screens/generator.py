import secrets
import string
import customtkinter as ctk
from tkinter import messagebox

from libs.window_manager import (
    BG,
    BORDER,
    DANGER,
    FONT,
    FONT_LG,
    FONT_MONO,
    FONT_TITLE,
    GOLD,
    ICON_GENERATOR,
    MUTED,
    PAD_X,
    SUCCESS,
    SURFACE,
    SURFACE2,
    TEXT,
    ScrollableFrame,
    make_button,
    make_card,
)


class GeneratorScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.controller = controller

        if not self.controller.master_key:
            self.after(0, lambda: self.controller.show_screen("login"))
            return

        self.length_var = ctk.IntVar(value=16)
        self.upper_var = ctk.BooleanVar(value=True)
        self.lower_var = ctk.BooleanVar(value=True)
        self.number_var = ctk.BooleanVar(value=True)
        self.symbol_var = ctk.BooleanVar(value=True)
        self.generated_var = ctk.StringVar(value="")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.build_header()
        self.build_generator()

    def build_header(self):
        top = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        top.grid(row=0, column=0, sticky="ew", padx=PAD_X, pady=(42, 18))
        top.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            top,
            text=f"{ICON_GENERATOR} Password Generator",
            font=FONT_TITLE,
            text_color=GOLD,
        ).grid(row=0, column=0, sticky="w")

        make_button(
            top,
            "Back",
            lambda: self.controller.show_screen("dashboard"),
            variant="secondary",
        ).grid(row=0, column=1, sticky="e", ipadx=18, ipady=7)

    def build_generator(self):
        scroll = ScrollableFrame(self, fg_color=BG)
        scroll.grid(row=1, column=0, sticky="nsew", padx=PAD_X, pady=(0, 42))
        scroll.content.grid_columnconfigure(0, weight=1)

        card = make_card(scroll.content)
        card.grid(row=0, column=0, sticky="ew")
        card.grid_columnconfigure(0, weight=1)

        body = ctk.CTkFrame(card, fg_color=SURFACE, corner_radius=0)
        body.grid(row=0, column=0, sticky="ew", padx=24, pady=24)
        body.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            body,
            text="Length",
            font=FONT_LG,
            text_color=TEXT,
        ).grid(row=0, column=0, sticky="w")

        length_row = ctk.CTkFrame(body, fg_color=SURFACE, corner_radius=0)
        length_row.grid(row=1, column=0, sticky="ew", pady=(8, 18))
        length_row.grid_columnconfigure(0, weight=1)

        ctk.CTkSlider(
            length_row,
            from_=8,
            to=32,
            variable=self.length_var,
            button_color=GOLD,
            button_hover_color="#D8BA5C",
            progress_color=GOLD,
            fg_color=SURFACE2,
        ).grid(row=0, column=0, sticky="ew")

        ctk.CTkLabel(
            length_row,
            textvariable=self.length_var,
            width=42,
            font=FONT_LG,
            text_color=GOLD,
        ).grid(row=0, column=1)

        options = ctk.CTkFrame(body, fg_color=SURFACE, corner_radius=0)
        options.grid(row=2, column=0, sticky="ew", pady=(0, 20))

        self.add_check(options, "Uppercase", self.upper_var)
        self.add_check(options, "Lowercase", self.lower_var)
        self.add_check(options, "Numbers", self.number_var)
        self.add_check(options, "Symbols", self.symbol_var)

        ctk.CTkEntry(
            body,
            textvariable=self.generated_var,
            font=FONT_MONO,
            fg_color=SURFACE2,
            text_color=TEXT,
            border_color=SURFACE2,
            corner_radius=6,
        ).grid(row=3, column=0, sticky="ew", ipady=5)

        self.build_strength_meter(body, start_row=4)

        actions = ctk.CTkFrame(body, fg_color=SURFACE, corner_radius=0)
        actions.grid(row=6, column=0, sticky="ew", pady=(20, 0))

        make_button(actions, "Generate", self.generate, font=FONT_LG).pack(side="left", ipadx=22, ipady=6)
        make_button(actions, "Copy", self.copy, variant="secondary").pack(side="left", padx=10, ipadx=18, ipady=6)

    def add_check(self, parent, text, variable):
        ctk.CTkCheckBox(
            parent,
            text=text,
            variable=variable,
            font=FONT,
            text_color=TEXT,
            fg_color=GOLD,
            hover_color="#D8BA5C",
            border_color=SURFACE2,
            checkmark_color="#161622",
        ).pack(side="left", padx=(0, 18))

    def build_strength_meter(self, parent, start_row):
        meter = ctk.CTkFrame(parent, fg_color=SURFACE, corner_radius=0)
        meter.grid(row=start_row, column=0, sticky="ew", pady=(12, 0))

        for index in range(4):
            meter.grid_columnconfigure(index, weight=1)

        self.meter_segments = []

        for index in range(4):
            segment = ctk.CTkFrame(meter, fg_color=BORDER, height=6, corner_radius=4)
            segment.grid(row=0, column=index, sticky="ew", padx=(0, 4))
            self.meter_segments.append(segment)

        self.strength_label = ctk.CTkLabel(
            parent,
            text="Password strength: empty",
            font=FONT,
            text_color=MUTED,
            anchor="w",
        )
        self.strength_label.grid(row=start_row + 1, column=0, sticky="ew", pady=(8, 0))

    def password_score(self, value):
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

    def update_strength(self):
        password = self.generated_var.get()
        score = self.password_score(password)

        labels = ["empty", "weak", "fair", "good", "strong"]
        colors = [BORDER, DANGER, "#D6A94F", GOLD, SUCCESS]

        for index, segment in enumerate(self.meter_segments):
            segment.configure(fg_color=colors[score] if index < score else BORDER)

        self.strength_label.configure(
            text=f"Password strength: {labels[score]}",
            text_color=colors[score],
        )

    def generate(self):
        pools = []

        if self.upper_var.get():
            pools.append(string.ascii_uppercase)
        if self.lower_var.get():
            pools.append(string.ascii_lowercase)
        if self.number_var.get():
            pools.append(string.digits)
        if self.symbol_var.get():
            pools.append("!@#$%^&*()-_=+[]{};:,.?")

        if not pools:
            messagebox.showwarning(
                "No character types",
                "Select at least one character type.",
            )
            return

        alphabet = "".join(pools)
        password = "".join(secrets.choice(alphabet) for _ in range(int(self.length_var.get())))

        self.generated_var.set(password)
        self.update_strength()

    def copy(self):
        password = self.generated_var.get()

        if not password:
            messagebox.showwarning("Nothing to copy", "Generate a password before copying.")
            return

        self.clipboard_clear()
        self.clipboard_append(password)
        messagebox.showinfo("Copied", "Generated password copied to clipboard.")