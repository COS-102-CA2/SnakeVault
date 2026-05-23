import tkinter as tk
from tkinter import messagebox, simpledialog

from db import delete_password, get_master_key
from libs.crypto import decrypt, verify_key
from libs.window_manager import (
    BG,
    BORDER,
    DANGER,
    FONT,
    FONT_LG,
    FONT_TITLE,
    GOLD,
    ICON_COPY,
    ICON_DELETE,
    ICON_KEY,
    MUTED,
    PAD_X,
    SURFACE,
    SURFACE2,
    TEXT,
    make_button,
    make_card,
)


class PasswordDetailScreen(tk.Frame):
    def __init__(self, parent, controller, entry):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.entry_data = entry
        self.verified_key = None
        self.hide_job = None

        if not self.controller.master_key:
            self.after(0, lambda: self.controller.show_screen("login"))
            return

        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        top = tk.Frame(self, bg=BG)
        top.grid(row=0, column=0, sticky="ew", padx=PAD_X, pady=(42, 18))
        top.columnconfigure(0, weight=1)

        tk.Label(
            top,
            text=f"{ICON_KEY} Password Details",
            font=FONT_TITLE,
            fg=GOLD,
            bg=BG,
        ).grid(row=0, column=0, sticky="w")

        make_button(
            top,
            "Back",
            lambda: controller.show_screen("dashboard"),
            variant="secondary",
        ).grid(row=0, column=1, sticky="e", ipadx=18, ipady=7)

        card = make_card(self)
        card.grid(row=1, column=0, sticky="nsew", padx=PAD_X, pady=(0, 42))
        card.columnconfigure(0, weight=1)

        body = tk.Frame(card, bg=SURFACE)
        body.grid(row=0, column=0, sticky="nsew", padx=24, pady=24)
        body.columnconfigure(0, weight=1)

        self.add_display(body, "Site", entry.get("site_name", ""), can_copy=True)
        self.add_display(body, "URL", entry.get("url", ""), can_copy=True)
        self.add_display(body, "Username", entry.get("username", ""), can_copy=True)
        self.password_value = self.add_display(body, "Password", "Hidden until verified", can_copy=True)
        self.add_display(body, "Category", entry.get("category", "General"))
        self.add_display(body, "Notes", entry.get("notes", ""))

        actions = tk.Frame(body, bg=SURFACE)
        actions.grid(row=12, column=0, sticky="ew", pady=(18, 0))
        actions.columnconfigure(0, weight=1)

        make_button(actions, "Reveal password", self.verify_before_reveal, font=FONT_LG).grid(row=0, column=0, sticky="w", ipadx=24, ipady=9)
        make_button(actions, f"{ICON_DELETE} Delete", self.delete_entry, variant="danger").grid(row=0, column=1, sticky="e", ipadx=22, ipady=9)

    def add_display(self, parent, label, value, can_copy=False):
        row_index = len(parent.grid_slaves())

        tk.Label(parent, text=label, font=FONT, fg=MUTED, bg=SURFACE, anchor="w").grid(
            row=row_index,
            column=0,
            sticky="ew",
            pady=(0, 5),
        )

        row = tk.Frame(parent, bg=SURFACE)
        row.grid(row=row_index + 1, column=0, sticky="ew", pady=(0, 12))
        row.columnconfigure(0, weight=1)

        value_label = tk.Label(
            row,
            text=value or "-",
            font=FONT_LG,
            fg=TEXT,
            bg=SURFACE2,
            anchor="w",
            padx=12,
            pady=8,
        )
        value_label.grid(row=0, column=0, sticky="ew")

        if can_copy:
            make_button(
                row,
                f"{ICON_COPY} Copy",
                lambda: self.copy_value(value_label.cget("text")),
                variant="secondary",
            ).grid(row=0, column=1, padx=(8, 0), ipadx=12, ipady=8)

        return value_label

    def verify_before_reveal(self):
        entered_key = simpledialog.askstring(
            "Verify master key",
            "Enter your master key:",
            show="*",
            parent=self,
        )

        if not entered_key:
            return

        result = get_master_key()

        if not result["success"] or not result["data"]:
            messagebox.showerror("Verification failed", result.get("error", "Could not verify master key."))
            return

        if not verify_key(entered_key, result["data"]):
            messagebox.showerror("Wrong key", "Incorrect master key.")
            return

        try:
            decrypted_password = decrypt(self.entry_data.get("encrypted_password", ""), entered_key)
        except Exception:
            messagebox.showerror("Decrypt failed", "Could not decrypt this password with the supplied key.")
            return

        self.verified_key = entered_key
        self.password_value.configure(text=decrypted_password)

        if self.hide_job:
            self.after_cancel(self.hide_job)

        self.hide_job = self.after(30000, self.hide_password)

    def hide_password(self):
        self.password_value.configure(text="Hidden until verified")
        self.verified_key = None
        self.hide_job = None

    def copy_value(self, value):
        if not value or value == "-" or value == "Hidden until verified":
            return

        self.clipboard_clear()
        self.clipboard_append(value)
        messagebox.showinfo("Copied", "Value copied to clipboard.")

    def delete_entry(self):
        confirm = messagebox.askyesno("Delete password", "Delete this saved credential?")

        if not confirm:
            return

        result = delete_password(self.entry_data.get("id"))

        if result["success"]:
            self.controller.show_screen("dashboard")
        else:
            messagebox.showerror("Delete failed", result.get("error", "Could not delete credential."))