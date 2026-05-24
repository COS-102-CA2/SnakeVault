import customtkinter as ctk
from tkinter import messagebox

from libs.db import fetch_user_passwords, get_master_key, logout_user, save_master_key, update_password
from libs.crypto import decrypt, encrypt, hash_key, verify_key
from libs.window_manager import (
    BG,
    BORDER,
    DANGER,
    FONT,
    FONT_LG,
    FONT_TITLE,
    GOLD,
    ICON_LOCK,
    ICON_SETTINGS,
    MUTED,
    PAD_X,
    SURFACE,
    TEXT,
    ScrollableFrame,
    make_button,
    make_card,
    make_entry,
    make_field_label,
)


class SettingsScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.controller = controller

        if not self.controller.master_key:
            self.after(0, lambda: self.controller.show_screen("login"))
            return

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.build_header()
        self.build_settings()

    def build_header(self):
        top = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        top.grid(row=0, column=0, sticky="ew", padx=PAD_X, pady=(42, 18))
        top.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            top,
            text=f"{ICON_SETTINGS} Settings",
            font=FONT_TITLE,
            text_color=GOLD,
        ).grid(row=0, column=0, sticky="w")

        make_button(
            top,
            "Back",
            lambda: self.controller.show_screen("dashboard"),
            variant="secondary",
        ).grid(row=0, column=1, sticky="e", ipadx=18, ipady=7)

    def build_settings(self):
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
            text="Change master key",
            font=FONT_LG,
            text_color=TEXT,
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            body,
            text="Changing the key will re-encrypt your saved passwords before updating Supabase.",
            font=FONT,
            text_color=MUTED,
        ).grid(row=1, column=0, sticky="w", pady=(2, 16))

        self.current_entry = self.add_field(body, "Current master key", 2)
        self.new_entry = self.add_field(body, "New master key", 4)
        self.confirm_entry = self.add_field(body, "Confirm new master key", 6)

        make_button(
            body,
            "Update master key",
            self.change_master_key,
            font=FONT_LG,
        ).grid(row=8, column=0, sticky="e", pady=(8, 24), ipadx=22, ipady=6)

        ctk.CTkFrame(
            body,
            fg_color=BORDER,
            height=1,
            corner_radius=0,
        ).grid(row=9, column=0, sticky="ew", pady=(4, 18))

        ctk.CTkLabel(
            body,
            text="Session",
            font=FONT_LG,
            text_color=TEXT,
        ).grid(row=10, column=0, sticky="w")

        make_button(
            body,
            f"{ICON_LOCK} Logout and lock vault",
            self.logout,
            variant="danger",
        ).grid(row=11, column=0, sticky="w", pady=(12, 0), ipadx=20, ipady=6)

    def add_field(self, parent, label, row):
        make_field_label(parent, label).grid(
            row=row,
            column=0,
            sticky="ew",
            pady=(0, 6),
        )

        entry = make_entry(parent, show="*")
        entry.grid(
            row=row + 1,
            column=0,
            sticky="ew",
            ipady=5,
            pady=(0, 12),
        )

        return entry

    def change_master_key(self):
        current = self.current_entry.get()
        new_key = self.new_entry.get()
        confirm = self.confirm_entry.get()

        if not current or not new_key or not confirm:
            messagebox.showwarning("Missing details", "Fill in all master key fields.")
            return

        if len(new_key) < 8:
            messagebox.showwarning("Weak key", "Use at least 8 characters for the new master key.")
            return

        if new_key != confirm:
            messagebox.showwarning("Keys do not match", "Confirm the new master key exactly.")
            return

        stored = get_master_key()

        if not stored["success"] or not stored["data"]:
            messagebox.showerror(
                "Verification failed",
                stored.get("error", "Could not verify current master key."),
            )
            return

        if not verify_key(current, stored["data"]):
            messagebox.showerror("Wrong key", "The current master key is incorrect.")
            self.current_entry.delete(0, "end")
            return

        entries = fetch_user_passwords()

        if not entries["success"]:
            messagebox.showerror(
                "Update failed",
                entries.get("error", "Could not load saved passwords."),
            )
            return

        for item in entries["data"]:
            try:
                plain_password = decrypt(item.get("encrypted_password", ""), current)
                encrypted_password = encrypt(plain_password, new_key)
            except Exception:
                messagebox.showerror(
                    "Update failed",
                    f"Could not re-encrypt {item.get('site_name', 'one entry')}.",
                )
                return

            result = update_password(
                item.get("id"),
                item.get("site_name", ""),
                item.get("url", ""),
                item.get("username", ""),
                encrypted_password,
                item.get("category") or "General",
                item.get("notes"),
            )

            if not result["success"]:
                messagebox.showerror(
                    "Update failed",
                    result.get("error", "Could not update one saved password."),
                )
                return

        save_result = save_master_key(hash_key(new_key))

        if not save_result["success"]:
            messagebox.showerror(
                "Update failed",
                save_result.get("error", "Could not save the new master key hash."),
            )
            return

        self.controller.master_key = new_key

        self.current_entry.delete(0, "end")
        self.new_entry.delete(0, "end")
        self.confirm_entry.delete(0, "end")

        messagebox.showinfo("Master key updated", "Your master key has been changed.")

    def logout(self):
        logout_user()
        self.controller.master_key = None
        self.controller.show_screen("login")