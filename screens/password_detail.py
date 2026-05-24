import customtkinter as ctk
from tkinter import messagebox, simpledialog

from libs.db import delete_password, get_master_key
from libs.crypto import decrypt, verify_key
from libs.window_manager import (
    BG,
    DANGER,
    FONT,
    FONT_LG,
    FONT_TITLE,
    GOLD,
    ICON_COPY,
    ICON_DELETE,
    ICON_EYE,
    ICON_EYE_OFF,
    ICON_KEY,
    MUTED,
    PAD_X,
    SURFACE,
    SURFACE2,
    TEXT,
    ScrollableFrame,
    make_button,
    make_card,
)


class PasswordDetailScreen(ctk.CTkFrame):
    def __init__(self, parent, controller, entry):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.controller = controller

        if not self.controller.master_key:
            self.after(0, lambda: self.controller.show_screen("login"))
            return

        self.entry_data = entry
        self.revealed_password = None
        self.hide_job = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.build_header()
        self.build_detail()

    def build_header(self):
        top = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        top.grid(row=0, column=0, sticky="ew", padx=PAD_X, pady=(42, 18))
        top.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            top,
            text=f"{ICON_KEY} Password Details",
            font=FONT_TITLE,
            text_color=GOLD,
        ).grid(row=0, column=0, sticky="w")

        make_button(
            top,
            "Back",
            lambda: self.controller.show_screen("dashboard"),
            variant="secondary",
        ).grid(row=0, column=1, sticky="e", ipadx=18, ipady=7)

    def build_detail(self):
        scroll = ScrollableFrame(self, fg_color=BG)
        scroll.grid(row=1, column=0, sticky="nsew", padx=PAD_X, pady=(0, 42))
        scroll.content.grid_columnconfigure(0, weight=1)

        card = make_card(scroll.content)
        card.grid(row=0, column=0, sticky="ew")
        card.grid_columnconfigure(0, weight=1)

        body = ctk.CTkFrame(card, fg_color=SURFACE, corner_radius=0)
        body.grid(row=0, column=0, sticky="ew", padx=24, pady=24)
        body.grid_columnconfigure(0, weight=1)

        self.add_display(body, "Site", self.entry_data.get("site_name", ""), can_copy=True)
        self.add_display(body, "URL", self.entry_data.get("url", ""), can_copy=True)
        self.add_display(body, "Username", self.entry_data.get("username", ""), can_copy=True)

        self.password_value = self.add_display(
            body,
            "Password",
            "Hidden until verified",
            password_row=True,
        )

        self.add_display(body, "Category", self.entry_data.get("category", "General"))
        self.add_display(body, "Notes", self.entry_data.get("notes", ""))

        actions = ctk.CTkFrame(body, fg_color=SURFACE, corner_radius=0)
        actions.grid(row=20, column=0, sticky="ew", pady=(18, 0))
        actions.grid_columnconfigure(0, weight=1)

        make_button(
            actions,
            f"{ICON_DELETE} Delete",
            self.delete_entry,
            variant="danger",
        ).grid(row=0, column=1, sticky="e", ipadx=22, ipady=6)

    def next_row(self, parent):
        rows = [
            child.grid_info()["row"]
            for child in parent.grid_slaves()
            if "row" in child.grid_info()
        ]

        if not rows:
            return 0

        return max(int(row) for row in rows) + 1

    def add_display(self, parent, label, value, can_copy=False, password_row=False):
        row_index = self.next_row(parent)

        ctk.CTkLabel(
            parent,
            text=label,
            font=FONT,
            text_color=MUTED,
            anchor="w",
        ).grid(row=row_index, column=0, sticky="ew", pady=(0, 5))

        row = ctk.CTkFrame(parent, fg_color=SURFACE, corner_radius=0)
        row.grid(row=row_index + 1, column=0, sticky="ew", pady=(0, 12))
        row.grid_columnconfigure(0, weight=1)

        value_label = ctk.CTkLabel(
            row,
            text=value or "-",
            font=FONT_LG,
            text_color=TEXT,
            fg_color=SURFACE2,
            corner_radius=6,
            anchor="w",
            padx=12,
            pady=8,
        )
        value_label.grid(row=0, column=0, sticky="ew")

        if password_row:
            self.reveal_btn = make_button(
                row,
                f"{ICON_EYE} Reveal",
                self.toggle_reveal_password,
                variant="secondary",
            )
            self.reveal_btn.grid(row=0, column=1, padx=(8, 0), ipadx=12, ipady=6)

            make_button(
                row,
                f"{ICON_COPY} Copy",
                self.copy_password,
                variant="secondary",
            ).grid(row=0, column=2, padx=(8, 0), ipadx=12, ipady=6)

        elif can_copy:
            make_button(
                row,
                f"{ICON_COPY} Copy",
                lambda: self.copy_value(value_label.cget("text")),
                variant="secondary",
            ).grid(row=0, column=1, padx=(8, 0), ipadx=12, ipady=6)

        return value_label

    def verify_and_decrypt(self):
        entered_key = simpledialog.askstring(
            "Verify master key",
            "Enter your master key:",
            show="*",
            parent=self,
        )

        if not entered_key:
            return None

        result = get_master_key()

        if not result["success"] or not result["data"]:
            messagebox.showerror(
                "Verification failed",
                result.get("error", "Could not verify master key."),
            )
            return None

        if not verify_key(entered_key, result["data"]):
            messagebox.showerror("Wrong key", "Incorrect master key.")
            return None

        try:
            return decrypt(
                self.entry_data.get("encrypted_password", ""),
                entered_key,
            )
        except Exception:
            messagebox.showerror(
                "Decrypt failed",
                "Could not decrypt this password with the supplied key.",
            )
            return None

    def toggle_reveal_password(self):
        if self.revealed_password:
            self.hide_password()
            return

        decrypted_password = self.verify_and_decrypt()

        if not decrypted_password:
            return

        self.revealed_password = decrypted_password
        self.password_value.configure(text=decrypted_password)
        self.reveal_btn.configure(text=f"{ICON_EYE_OFF} Hide")

        if self.hide_job:
            self.after_cancel(self.hide_job)

        self.hide_job = self.after(30000, self.hide_password)

    def hide_password(self):
        self.revealed_password = None
        self.password_value.configure(text="Hidden until verified")
        self.reveal_btn.configure(text=f"{ICON_EYE} Reveal")

        if self.hide_job:
            self.after_cancel(self.hide_job)

        self.hide_job = None

    def copy_password(self):
        password = self.revealed_password

        if not password:
            password = self.verify_and_decrypt()

        if not password:
            return

        self.clipboard_clear()
        self.clipboard_append(password)
        messagebox.showinfo("Copied", "Password copied to clipboard.")

    def copy_value(self, value):
        if not value or value == "-" or value == "Hidden until verified":
            return

        self.clipboard_clear()
        self.clipboard_append(value)
        messagebox.showinfo("Copied", "Value copied to clipboard.")

    def delete_entry(self):
        confirm = messagebox.askyesno(
            "Delete password",
            "Delete this saved credential?",
        )

        if not confirm:
            return

        result = delete_password(self.entry_data.get("id"))

        if result["success"]:
            self.controller.show_screen("dashboard")
        else:
            messagebox.showerror(
                "Delete failed",
                result.get("error", "Could not delete credential."),
            )