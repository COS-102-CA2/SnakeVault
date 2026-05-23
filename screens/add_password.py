import secrets
import string
import tkinter as tk
from tkinter import messagebox

from db import save_password
from libs.crypto import encrypt
from libs.window_manager import (
    BG,
    BORDER,
    CARD_PAD_X,
    CARD_PAD_Y,
    FONT,
    FONT_LG,
    FONT_TITLE,
    GOLD,
    ICON_GENERATOR,
    ICON_PLUS,
    MUTED,
    PAD_X,
    SURFACE,
    SURFACE2,
    TEXT,
    make_button,
    make_card,
    make_entry,
    make_field_label,
)


class AddPasswordScreen(tk.Frame):
    def _init_(self, parent, controller):
        super()._init_(parent, bg=BG)
        self.controller = controller
        self.show_password = False

        if not self.controller.master_key:
            self.after(0, lambda: self.controller.show_screen("login"))
            return

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        self.build_header()
        self.build_form()

    def build_header(self):
        header = tk.Frame(self, bg=BG)
        header.grid(row=0, column=0, sticky="ew", padx=PAD_X, pady=(28, 14))
        header.columnconfigure(0, weight=1)

        tk.Label(
            header,
            text=f"{ICON_PLUS} Add Password",
            font=FONT_TITLE,
            fg=GOLD,
            bg=BG,
        ).grid(row=0, column=0, sticky="w")

        make_button(
            header,
            "Back",
            lambda: self.controller.show_screen("dashboard"),
            variant="secondary",
        ).grid(row=0, column=1, sticky="e", ipadx=18, ipady=7)

    def build_form(self):
        card = make_card(self)
        card.grid(row=1, column=0, sticky="nsew", padx=PAD_X, pady=(0, 24))
        card.columnconfigure(0, weight=1)
        card.rowconfigure(0, weight=1)

        form = tk.Frame(card, bg=SURFACE)
        form.grid(row=0, column=0, sticky="nsew", padx=CARD_PAD_X, pady=CARD_PAD_Y)
        form.columnconfigure(0, weight=1)
        form.columnconfigure(1, weight=1)

        self.site_entry = self.add_field(form, "Site name", 0, 0)
        self.url_entry = self.add_field(form, "URL", 0, 1)
        self.username_entry = self.add_field(form, "Username or email", 1, 0)
        self.category_entry = self.add_field(form, "Category", 1, 1, default="General")

        make_field_label(form, "Password").grid(row=2, column=0, columnspan=2, sticky="ew", pady=(8, 6))

        password_row = tk.Frame(form, bg=SURFACE)
        password_row.grid(row=3, column=0, columnspan=2, sticky="ew")
        password_row.columnconfigure(0, weight=1)

        self.password_entry = make_entry(password_row, show="*")
        self.password_entry.grid(row=0, column=0, sticky="ew", ipady=8)

        make_button(
            password_row,
            "Show",
            self.toggle_password,
            variant="secondary",
        ).grid(row=0, column=1, padx=(8, 0), ipadx=12, ipady=7)

        make_button(
            password_row,
            f"{ICON_GENERATOR} Generate",
            self.generate_password,
            variant="primary",
        ).grid(row=0, column=2, padx=(8, 0), ipadx=16, ipady=7)

        make_field_label(form, "Notes").grid(row=4, column=0, columnspan=2, sticky="ew", pady=(14, 6))

        self.notes_entry = tk.Text(
            form,
            height=4,
            font=FONT,
            bg=SURFACE2,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            wrap="word",
        )
        self.notes_entry.grid(row=5, column=0, columnspan=2, sticky="nsew")
        form.rowconfigure(5, weight=1)

        actions = tk.Frame(form, bg=SURFACE)
        actions.grid(row=6, column=0, columnspan=2, sticky="ew", pady=(18, 0))
        actions.columnconfigure(0, weight=1)

        tk.Label(
            actions,
            text="Site, username, and password are required.",
            font=FONT,
            fg=MUTED,
            bg=SURFACE,
        ).grid(row=0, column=0, sticky="w")

        make_button(
            actions,
            "Save to vault",
            self.save,
            variant="primary",
            font=FONT_LG,
        ).grid(row=0, column=1, sticky="e", ipadx=28, ipady=9)

    def add_field(self, parent, label, row, column, default=""):
        make_field_label(parent, label).grid(row=row * 2, column=column, sticky="ew", pady=(0, 6), padx=(0, 10))

        entry = make_entry(parent)
        entry.grid(row=row * 2 + 1, column=column, sticky="ew", ipady=8, padx=(0, 10), pady=(0, 10))

        if default:
            entry.insert(0, default)

        return entry

    def toggle_password(self):
        self.show_password = not self.show_password
        self.password_entry.configure(show="" if self.show_password else "*")

    def generate_password(self):
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:,.?"
        password = "".join(secrets.choice(alphabet) for _ in range(16))

        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def save(self):
        site = self.site_entry.get().strip()
        url = self.url_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        category = self.category_entry.get().strip() or "General"
        notes = self.notes_entry.get("1.0", tk.END).strip()

        if not site or not username or not password:
            messagebox.showwarning(
                "Missing details",
                "Site, username, and password are required.",
            )
            return

        encrypted_password = encrypt(password, self.controller.master_key)

        result = save_password(
            site,
            url,
            username,
            encrypted_password,
            category,
            notes,
        )

        if result["success"]:
            messagebox.showinfo(
                "Saved",
                "Credential saved securely.",
            )
            self.controller.show_screen("dashboard")
        else:
            messagebox.showerror(
                "Save failed",
                result.get("error", "Could not save credential."),
            )