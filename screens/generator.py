import secrets
import string
import tkinter as tk
from tkinter import messagebox

from libs.window_manager import BG, BORDER, GOLD, MUTED, SURFACE, SURFACE2, TEXT, FONT, FONT_LG, FONT_TITLE


class GeneratorScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        self.length_var = tk.IntVar(value=16)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.number_var = tk.BooleanVar(value=True)
        self.symbol_var = tk.BooleanVar(value=True)
        self.generated_var = tk.StringVar(value="")

        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=54, pady=(42, 18))

        tk.Label(
            top,
            text="Password Generator",
            font=FONT_TITLE,
            fg=GOLD,
            bg=BG,
        ).pack(side="left")

        tk.Button(
            top,
            text="Back",
            font=FONT,
            bg=SURFACE2,
            fg=TEXT,
            bd=0,
            command=lambda: controller.show_screen("dashboard"),
        ).pack(side="right", ipadx=18, ipady=7)

        card = tk.Frame(
            self,
            bg=SURFACE,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        card.pack(fill="both", expand=True, padx=54, pady=(0, 42))

        body = tk.Frame(card, bg=SURFACE)
        body.pack(fill="both", expand=True, padx=24, pady=24)

        tk.Label(
            body,
            text="Length",
            font=FONT_LG,
            fg=TEXT,
            bg=SURFACE,
        ).pack(anchor="w")

        length_row = tk.Frame(body, bg=SURFACE)
        length_row.pack(fill="x", pady=(8, 18))

        tk.Scale(
            length_row,
            from_=8,
            to=32,
            orient="horizontal",
            variable=self.length_var,
            bg=SURFACE,
            fg=TEXT,
            troughcolor=SURFACE2,
            highlightthickness=0,
        ).pack(side="left", fill="x", expand=True)

        tk.Label(
            length_row,
            textvariable=self.length_var,
            width=4,
            font=FONT_LG,
            fg=GOLD,
            bg=SURFACE,
        ).pack(side="left")

        options = tk.Frame(body, bg=SURFACE)
        options.pack(fill="x", pady=(0, 20))

        self.add_check(options, "Uppercase", self.upper_var)
        self.add_check(options, "Lowercase", self.lower_var)
        self.add_check(options, "Numbers", self.number_var)
        self.add_check(options, "Symbols", self.symbol_var)

        tk.Entry(
            body,
            textvariable=self.generated_var,
            font=("Consolas", 15),
            bg=SURFACE2,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
        ).pack(fill="x", ipady=10)

        actions = tk.Frame(body, bg=SURFACE)
        actions.pack(fill="x", pady=(20, 0))

        tk.Button(
            actions,
            text="Generate",
            font=FONT_LG,
            bg=GOLD,
            fg="#161622",
            bd=0,
            command=self.generate,
        ).pack(side="left", ipadx=28, ipady=9)

        tk.Button(
            actions,
            text="Copy",
            font=FONT,
            bg=SURFACE2,
            fg=TEXT,
            bd=0,
            command=self.copy,
        ).pack(side="left", padx=10, ipadx=24, ipady=9)

    def add_check(self, parent, text, variable):
        tk.Checkbutton(
            parent,
            text=text,
            variable=variable,
            font=FONT,
            bg=SURFACE,
            fg=TEXT,
            selectcolor=SURFACE2,
            activebackground=SURFACE,
            activeforeground=TEXT,
        ).pack(side="left", padx=(0, 18))

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

            password = "".join(
                secrets.choice(alphabet)
                for _ in range(self.length_var.get())
            )

            self.generated_var.set(password)

    def copy(self):
        pass
