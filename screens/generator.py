import secrets
import string
import tkinter as tk
from tkinter import messagebox

from libs.window_manager import (
    BG,
    FONT,
    FONT_LG,
    FONT_MONO,
    FONT_TITLE,
    GOLD,
    ICON_GENERATOR,
    PAD_X,
    SURFACE,
    SURFACE2,
    TEXT,
    ScrollableFrame,
    make_button,
    make_card,
)


class GeneratorScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        if not self.controller.master_key:
            self.after(0, lambda: self.controller.show_screen("login"))
            return

        self.length_var = tk.IntVar(value=16)
        self.upper_var = tk.BooleanVar(value=True)
        self.lower_var = tk.BooleanVar(value=True)
        self.number_var = tk.BooleanVar(value=True)
        self.symbol_var = tk.BooleanVar(value=True)
        self.generated_var = tk.StringVar(value="")

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.build_header()
        self.build_generator()

    def build_header(self):
        top = tk.Frame(self, bg=BG)
        top.grid(row=0, column=0, sticky="ew", padx=PAD_X, pady=(42, 18))
        top.columnconfigure(0, weight=1)

        tk.Label(
            top,
            text=f"{ICON_GENERATOR} Password Generator",
            font=FONT_TITLE,
            fg=GOLD,
            bg=BG,
        ).grid(row=0, column=0, sticky="w")

        make_button(
            top,
            "Back",
            lambda: self.controller.show_screen("dashboard"),
            variant="secondary",
        ).grid(row=0, column=1, sticky="e", ipadx=18, ipady=7)

    def build_generator(self):
        scroll = ScrollableFrame(self, bg=BG)
        scroll.grid(row=1, column=0, sticky="nsew", padx=PAD_X, pady=(0, 42))
        scroll.content.columnconfigure(0, weight=1)

        card = make_card(scroll.content)
        card.grid(row=0, column=0, sticky="ew")
        card.columnconfigure(0, weight=1)

        body = tk.Frame(card, bg=SURFACE)
        body.grid(row=0, column=0, sticky="ew", padx=24, pady=24)
        body.columnconfigure(0, weight=1)

        tk.Label(
            body,
            text="Length",
            font=FONT_LG,
            fg=TEXT,
            bg=SURFACE,
        ).grid(row=0, column=0, sticky="w")

        length_row = tk.Frame(body, bg=SURFACE)
        length_row.grid(row=1, column=0, sticky="ew", pady=(8, 18))
        length_row.columnconfigure(0, weight=1)

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
        ).grid(row=0, column=0, sticky="ew")

        tk.Label(
            length_row,
            textvariable=self.length_var,
            width=4,
            font=FONT_LG,
            fg=GOLD,
            bg=SURFACE,
        ).grid(row=0, column=1)

        options = tk.Frame(body, bg=SURFACE)
        options.grid(row=2, column=0, sticky="ew", pady=(0, 20))

        self.add_check(options, "Uppercase", self.upper_var)
        self.add_check(options, "Lowercase", self.lower_var)
        self.add_check(options, "Numbers", self.number_var)
        self.add_check(options, "Symbols", self.symbol_var)

        tk.Entry(
            body,
            textvariable=self.generated_var,
            font=FONT_MONO,
            bg=SURFACE2,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
        ).grid(row=3, column=0, sticky="ew", ipady=10)

        actions = tk.Frame(body, bg=SURFACE)
        actions.grid(row=4, column=0, sticky="ew", pady=(20, 0))

        make_button(
            actions,
            "Generate",
            self.generate,
            font=FONT_LG,
        ).pack(side="left", ipadx=28, ipady=9)

        make_button(
            actions,
            "Copy",
            self.copy,
            variant="secondary",
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
        password = self.generated_var.get()

        if not password:
            messagebox.showwarning(
                "Nothing to copy",
                "Generate a password before copying.",
            )
            return

        self.clipboard_clear()
        self.clipboard_append(password)

        messagebox.showinfo(
            "Copied",
            "Generated password copied to clipboard.",
        )