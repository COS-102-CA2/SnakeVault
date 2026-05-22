import tkinter as tk
from tkinter import messagebox,simpledialog
from libs.db import get_master_key
from libs.crypto import verify_key

from libs.window_manager import BG, BORDER, GOLD, MUTED, SURFACE, SURFACE2, TEXT, FONT, FONT_LG, FONT_TITLE


class PasswordDetailScreen(tk.Frame):
    def __init__(self, parent, controller, entry):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.entry_data = entry
        self.verified_key=None

        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=54, pady=(42, 18))

        tk.Label(
            top,
            text="Password Details",
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

        self.add_display(body, "Site", entry.get("site_name", ""), can_copy=True)
        self.add_display(body, "URL", entry.get("url", ""), can_copy=True)
        self.add_display(body, "Username", entry.get("username", ""), can_copy=True)
        self.password_value = self.add_display(
            body,
            "Password",
            "Hidden until verified",
            can_copy=True,
        )
        self.add_display(body, "Category", entry.get("category", "General"))
        self.add_display(body, "Notes", entry.get("notes", ""))
        actions = tk.Frame(body, bg=SURFACE)
        actions.pack(fill="x", pady=(20, 0))

        tk.Button(
            actions,
            text="Reveal password",
            font=FONT_LG,
            bg=GOLD,
            fg="#161622",
            bd=0,
            command=self.verify_before_reveal,
        ).pack(side="left", ipadx=24, ipady=9)

    def add_display(self, parent, label, value, can_copy=False):
        tk.Label(
            parent,
            text=label,
            font=FONT,
            fg=MUTED,
            bg=SURFACE,
            anchor="w",
        ).pack(fill="x")

        row = tk.Frame(parent, bg=SURFACE)
        row.pack(fill="x", pady=(5, 12))

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
        value_label.pack(side="left", fill="x", expand=True)

        if can_copy:
            tk.Button(
                row,
                text="Copy",
                font=FONT,
                bg=SURFACE2,
                fg=TEXT,
                bd=0,
                command=lambda: self.copy_value(value_label.cget("text")),
            ).pack(side="left", padx=(8, 0), ipadx=12, ipady=8)

        return value_label

    def copy_value(self, value):
        if not value or value == "-" or value == "Hidden until verified":
            return

        self.clipboard_clear()
        self.clipboard_append(value)

        messagebox.showinfo(
            "Copied",
            "Value copied to clipboard.",
        )


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
            messagebox.showerror(
                "Verification failed",
                result.get("error", "Could not verify master key."),
            )
            return

         if not verify_key(entered_key, result["data"]):
            messagebox.showerror(
                "Wrong key",
                "Incorrect master key.",
            )
            return

         self.verified_key = entered_key

         messagebox.showinfo(
            "Verified",
            "Master key verified. Password reveal will be added next.",
         )