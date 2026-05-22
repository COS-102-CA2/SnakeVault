import tkinter as tk
from tkinter import messagebox

from libs.db import fetch_user_passwords, get_master_key, logout_user, save_master_key, update_password
from libs.crypto import decrypt, encrypt, hash_key, verify_key
from libs.window_manager import BG, BORDER, DANGER, GOLD, MUTED, SURFACE, SURFACE2, TEXT, FONT, FONT_LG, FONT_TITLE


class SettingsScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=54, pady=(42, 18))

        tk.Label(
            top,
            text="Settings",
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
            text="Change master key",
            font=FONT_LG,
            fg=TEXT,
            bg=SURFACE,
        ).pack(anchor="w")

        tk.Label(
            body,
            text="Changing the key will re-encrypt your saved passwords before updating Supabase.",
            font=FONT,
            fg=MUTED,
            bg=SURFACE,
        ).pack(anchor="w", pady=(2, 16))

        self.current_entry = self.add_field(
            body,
            "Current master key",
            show="*",
        )

        self.new_entry = self.add_field(
            body,
            "New master key",
            show="*",
        )

        self.confirm_entry = self.add_field(
            body,
            "Confirm new master key",
            show="*",
        )

        tk.Button(
            body,
            text="Update master key",
            font=FONT_LG,
            bg=GOLD,
            fg="#161622",
            bd=0,
            command=self.change_master_key,
        ).pack(anchor="e", pady=(8, 24), ipadx=26, ipady=9)

        tk.Frame(
            body,
            bg=BORDER,
            height=1,
        ).pack(fill="x", pady=(4, 18))

        tk.Label(
            body,
            text="Session",
            font=FONT_LG,
            fg=TEXT,
            bg=SURFACE,
        ).pack(anchor="w")

        tk.Button(
            body,
            text="Logout and lock vault",
            font=FONT,
            bg=DANGER,
            fg="#11111b",
            bd=0,
            command=self.logout,
        ).pack(anchor="w", pady=(12, 0), ipadx=24, ipady=9)

    def add_field(self, parent, label, show=None):
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
            show=show,
        )
        entry.pack(fill="x", pady=(6, 12), ipady=8)

        return entry

    def change_master_key(self):
        current = self.current_entry.get()
        new_key = self.new_entry.get()
        confirm = self.confirm_entry.get()

        if not current or not new_key or not confirm:
            messagebox.showwarning(
                "Missing details",
                "Fill in all master key fields.",
            )
            return

        if len(new_key) < 8:
            messagebox.showwarning(
                "Weak key",
                "Use at least 8 characters for the new master key.",
            )
            return

        if new_key != confirm:
            messagebox.showwarning(
                "Keys do not match",
                "Confirm the new master key exactly.",
            )
            return

        stored = get_master_key()

        if not stored["success"] or not stored["data"]:
            messagebox.showerror(
                "Verification failed",
                stored.get("error", "Could not verify current master key."),
            )
            return

        if not verify_key(current, stored["data"]):
            messagebox.showerror(
                "Wrong key",
                "The current master key is incorrect.",
            )
            self.current_entry.delete(0, tk.END)
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
                plain_password = decrypt(
                    item.get("encrypted_password", ""),
                    current,
                )

                encrypted_password = encrypt(
                    plain_password,
                    new_key,
                )
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

        self.current_entry.delete(0, tk.END)
        self.new_entry.delete(0, tk.END)
        self.confirm_entry.delete(0, tk.END)

        messagebox.showinfo(
            "Master key updated",
            "Your master key has been changed.",
        )

    def logout(self):
        logout_user()
        self.controller.master_key = None
        self.controller.show_screen("login")