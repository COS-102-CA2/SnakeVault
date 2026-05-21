import tkinter as tk
from tkinter import messagebox

from db import save_password
from libs.crypto import encrypt
from libs.window_manager import BG, BORDER, GOLD, MUTED, SURFACE, SURFACE2, TEXT, FONT, FONT_LG, FONT_TITLE


class AddPasswordScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.show_password = False

        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=54, pady=(36, 18))

        tk.Label(
            top,
            text="Add Password",
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
        card.pack(fill="both", expand=True, padx=54, pady=(0, 30))

        form = tk.Frame(card, bg=SURFACE)
        form.pack(fill="both", expand=True, padx=24, pady=22)

        self.site_entry = self.add_field(form, "Site name")
        self.url_entry = self.add_field(form, "URL")
        self.username_entry = self.add_field(form, "Username or email")

        tk.Label(
            form,
            text="Password",
            font=FONT,
            fg=MUTED,
            bg=SURFACE,
            anchor="w",
        ).pack(fill="x")

        password_row = tk.Frame(form, bg=SURFACE)
        password_row.pack(fill="x", pady=(6, 12))

        self.password_entry = tk.Entry(
            password_row,
            font=FONT,
            bg=SURFACE2,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            show="*",
        )
        self.password_entry.pack(side="left", fill="x", expand=True, ipady=8)

        tk.Button(
            password_row,
            text="Show",
            font=FONT,
            bg=SURFACE2,
            fg=TEXT,
            bd=0,
            command=self.toggle_password,
        ).pack(side="left", padx=(8, 0), ipadx=12, ipady=7)

        self.category_entry = self.add_field(form, "Category", default="General")
        self.notes_entry = self.add_field(form, "Notes")

        tk.Button(
            form,
            text="Save to vault",
            font=FONT_LG,
            bg=GOLD,
            fg="#161622",
            bd=0,
            command=self.save,
        ).pack(anchor="e", pady=(10, 0), ipadx=30, ipady=9)

    def add_field(self, parent, label, default=""):
        tk.Label(
            parent,
            text=label,
            font=FONT,
            fg=MUTED,
            bg=SURFACE,
            anchor="w",
        ).pack(fill="x")

        entry = tk.Entry(
            parent,
            font=FONT,
            bg=SURFACE2,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
        )
        entry.pack(fill="x", pady=(6, 12), ipady=8)

        if default:
            entry.insert(0, default)

        return entry

    def toggle_password(self):
        self.show_password = not self.show_password
        self.password_entry.configure(
            show="" if self.show_password else "*"
        )

    def save(self):
        site = self.site_entry.get().strip()
        url = self.url_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        category = self.category_entry.get().strip() or "General"
        notes = self.notes_entry.get().strip()

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