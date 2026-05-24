import secrets
import string
import customtkinter as ctk
from tkinter import messagebox

from libs.db import save_password
from libs.crypto import encrypt
from libs.window_manager import (
    BG,
    BORDER,
    CARD_PAD_X,
    CARD_PAD_Y,
    DANGER,
    FONT,
    FONT_LG,
    FONT_TITLE,
    GOLD,
    ICON_EYE,
    ICON_EYE_OFF,
    ICON_GENERATOR,
    ICON_PLUS,
    MUTED,
    PAD_X,
    SUCCESS,
    SURFACE,
    SURFACE2,
    TEXT,
    ScrollableFrame,
    make_button,
    make_card,
    make_entry,
    make_field_label,
    make_textbox,
)


class AddPasswordScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.controller = controller
        self.show_password = False

        if not self.controller.master_key:
            self.after(0, lambda: self.controller.show_screen("login"))
            return

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.build_header()
        self.build_form()

    def build_header(self):
        header = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        header.grid(row=0, column=0, sticky="ew", padx=PAD_X, pady=(28, 14))
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text=f"{ICON_PLUS} Add Password",
            font=FONT_TITLE,
            text_color=GOLD,
        ).grid(row=0, column=0, sticky="w")

        make_button(
            header,
            "Back",
            lambda: self.controller.show_screen("dashboard"),
            variant="secondary",
        ).grid(row=0, column=1, sticky="e", ipadx=18, ipady=7)

    def build_form(self):
        scroll = ScrollableFrame(self, fg_color=BG)
        scroll.grid(row=1, column=0, sticky="nsew", padx=PAD_X, pady=(0, 24))
        scroll.content.grid_columnconfigure(0, weight=1)

        card = make_card(scroll.content)
        card.grid(row=0, column=0, sticky="ew")
        card.grid_columnconfigure(0, weight=1)

        form = ctk.CTkFrame(card, fg_color=SURFACE, corner_radius=0)
        form.grid(row=0, column=0, sticky="ew", padx=CARD_PAD_X, pady=CARD_PAD_Y)
        form.grid_columnconfigure(0, weight=1)
        form.grid_columnconfigure(1, weight=1)

        self.site_entry = self.add_field(form, "Site name", 0, 0)
        self.url_entry = self.add_field(form, "URL", 0, 1)
        self.username_entry = self.add_field(form, "Username or email", 2, 0)
        self.category_entry = self.add_field(form, "Category", 2, 1, default="General")

        make_field_label(form, "Password").grid(row=4, column=0, columnspan=2, sticky="ew", pady=(8, 6))

        password_row = ctk.CTkFrame(form, fg_color=SURFACE, corner_radius=0)
        password_row.grid(row=5, column=0, columnspan=2, sticky="ew")
        password_row.grid_columnconfigure(0, weight=1)

        self.password_entry = make_entry(password_row, show="*")
        self.password_entry.grid(row=0, column=0, sticky="ew", ipady=5)
        self.password_entry.bind("<KeyRelease>", self.update_strength)

        self.toggle_btn = make_button(
            password_row,
            f"{ICON_EYE} Show",
            self.toggle_password,
            variant="secondary",
        )
        self.toggle_btn.grid(row=0, column=1, padx=(8, 0), ipadx=12, ipady=5)

        make_button(
            password_row,
            f"{ICON_GENERATOR} Generate",
            self.generate_password,
            variant="primary",
        ).grid(row=0, column=2, padx=(8, 0), ipadx=16, ipady=5)

        self.build_strength_meter(form, start_row=6)

        make_field_label(form, "Notes").grid(row=9, column=0, columnspan=2, sticky="ew", pady=(14, 6))

        self.notes_entry = make_textbox(form, height=120)
        self.notes_entry.grid(row=10, column=0, columnspan=2, sticky="ew")

        actions = ctk.CTkFrame(form, fg_color=SURFACE, corner_radius=0)
        actions.grid(row=11, column=0, columnspan=2, sticky="ew", pady=(18, 0))
        actions.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            actions,
            text="Site, username, and password are required.",
            font=FONT,
            text_color=MUTED,
        ).grid(row=0, column=0, sticky="w")

        make_button(
            actions,
            "Save to vault",
            self.save,
            variant="primary",
            font=FONT_LG,
        ).grid(row=0, column=1, sticky="e", ipadx=28, ipady=6)

    def add_field(self, parent, label, row, column, default=""):
        make_field_label(parent, label).grid(row=row, column=column, sticky="ew", pady=(0, 6), padx=(0, 10))

        entry = make_entry(parent)
        entry.grid(row=row + 1, column=column, sticky="ew", ipady=5, padx=(0, 10), pady=(0, 10))

        if default:
            entry.insert(0, default)

        return entry

    def build_strength_meter(self, parent, start_row):
        meter = ctk.CTkFrame(parent, fg_color=SURFACE, corner_radius=0)
        meter.grid(row=start_row, column=0, columnspan=2, sticky="ew", pady=(12, 0))

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
        self.strength_label.grid(row=start_row + 1, column=0, columnspan=2, sticky="ew", pady=(8, 0))

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

    def update_strength(self, _event=None):
        password = self.password_entry.get()
        score = self.password_score(password)

        labels = ["empty", "weak", "fair", "good", "strong"]
        colors = [BORDER, DANGER, "#D6A94F", GOLD, SUCCESS]

        for index, segment in enumerate(self.meter_segments):
            segment.configure(fg_color=colors[score] if index < score else BORDER)

        self.strength_label.configure(
            text=f"Password strength: {labels[score]}",
            text_color=colors[score],
        )

    def toggle_password(self):
        self.show_password = not self.show_password
        self.password_entry.configure(show="" if self.show_password else "*")
        self.toggle_btn.configure(
            text=f"{ICON_EYE_OFF} Hide" if self.show_password else f"{ICON_EYE} Show"
        )

    def generate_password(self):
        alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{};:,.?"
        password = "".join(secrets.choice(alphabet) for _ in range(16))

        self.password_entry.delete(0, "end")
        self.password_entry.insert(0, password)
        self.update_strength()

    def save(self):
        site = self.site_entry.get().strip()
        url = self.url_entry.get().strip()
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        category = self.category_entry.get().strip() or "General"
        notes = self.notes_entry.get("1.0", "end").strip()

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
            messagebox.showinfo("Saved", "Credential saved securely.")
            self.controller.show_screen("dashboard")
        else:
            messagebox.showerror(
                "Save failed",
                result.get("error", "Could not save credential."),
            )