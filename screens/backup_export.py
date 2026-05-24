import csv
import json
from datetime import datetime
import customtkinter as ctk
from tkinter import filedialog, messagebox, simpledialog

from libs.db import fetch_user_passwords, get_master_key
from libs.crypto import decrypt, verify_key
from libs.window_manager import (
    BG,
    BORDER,
    DANGER,
    FONT,
    FONT_LG,
    FONT_SM,
    FONT_TITLE,
    GOLD,
    ICON_COPY,
    ICON_LOCK,
    ICON_WARNING,
    MUTED,
    PAD_X,
    SUCCESS,
    SURFACE,
    TEXT,
    make_button,
    make_card,
)


class BackupExportScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.controller = controller

        if not self.controller.master_key:
            self.after(0, lambda: self.controller.show_screen("login"))
            return

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.build_header()
        self.build_status()
        self.build_cards()

    def build_header(self):
        ctk.CTkLabel(
            self,
            text="Backup & Export",
            font=FONT_TITLE,
            text_color=GOLD,
        ).grid(row=0, column=0, pady=(36, 6))

        ctk.CTkLabel(
            self,
            text="Settings -> Data",
            font=FONT,
            text_color=MUTED,
        ).grid(row=1, column=0, pady=(0, 18))

    def build_status(self):
        status = make_card(self)
        status.grid(row=2, column=0, sticky="ew", padx=PAD_X, pady=(0, 12))
        status.grid_columnconfigure(1, weight=1)

        ctk.CTkLabel(
            status,
            text="✅",
            font=("Segoe UI Emoji", 24),
            text_color=SUCCESS,
        ).grid(row=0, column=0, padx=(18, 12), pady=14)

        ctk.CTkLabel(
            status,
            text="Ready to create a backup",
            font=FONT_LG,
            text_color=SUCCESS,
            anchor="w",
        ).grid(row=0, column=1, sticky="w", pady=(12, 0))

        ctk.CTkLabel(
            status,
            text="Encrypted backups are safe to store. Plain CSV exports are not encrypted.",
            font=FONT_SM,
            text_color=MUTED,
            anchor="w",
        ).grid(row=1, column=1, sticky="w", pady=(0, 12))

    def build_cards(self):
        grid = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        grid.grid(row=3, column=0, sticky="nsew", padx=PAD_X, pady=(0, 14))

        for index in range(3):
            grid.grid_columnconfigure(index, weight=1)

        encrypted = self.option_card(grid, 0, f"{ICON_LOCK} Encrypted backup (.svb)")
        ctk.CTkLabel(
            encrypted,
            text="Export your vault as a fully encrypted file.\nSafe to store in cloud or email to yourself.",
            font=FONT,
            text_color=MUTED,
            justify="left",
        ).pack(anchor="w", padx=14, pady=(4, 18))

        make_button(
            encrypted,
            "Export encrypted ->",
            self.export_encrypted,
        ).pack(anchor="w", padx=14, pady=(0, 14), ipadx=14, ipady=6)

        csv_card = self.option_card(grid, 1, f"{ICON_WARNING} Export CSV (plain text)", danger=True)
        ctk.CTkLabel(
            csv_card,
            text="WARNING: This file is NOT encrypted.\nDelete immediately after use.",
            font=FONT,
            text_color=MUTED,
            justify="left",
        ).pack(anchor="w", padx=14, pady=(4, 18))

        make_button(
            csv_card,
            "Export CSV ->",
            self.export_csv,
            variant="danger",
        ).pack(anchor="w", padx=14, pady=(0, 14), ipadx=14, ipady=6)

        import_card = self.option_card(grid, 2, f"{ICON_COPY} Import")
        ctk.CTkLabel(
            import_card,
            text="Restore from a .svb file.\nImport support can be added later.",
            font=FONT,
            text_color=MUTED,
            justify="left",
        ).pack(anchor="w", padx=14, pady=(4, 18))

        make_button(
            import_card,
            "Choose file ->",
            self.import_placeholder,
            variant="secondary",
        ).pack(anchor="w", padx=14, pady=(0, 14), ipadx=14, ipady=6)

        make_button(
            self,
            "<- Back to settings",
            lambda: self.controller.show_screen("settings"),
            variant="secondary",
            font=FONT_LG,
        ).grid(row=4, column=0, sticky="e", padx=PAD_X, pady=(0, 14), ipadx=24, ipady=7)

    def option_card(self, parent, column, title, danger=False):
        card = ctk.CTkFrame(
            parent,
            fg_color=SURFACE,
            border_color=DANGER if danger else BORDER,
            border_width=1,
            corner_radius=8,
        )
        card.grid(row=0, column=column, sticky="nsew", padx=(0, 10))
        card.grid_propagate(False)
        card.configure(height=245)

        ctk.CTkLabel(
            card,
            text=title,
            font=FONT_LG,
            text_color=TEXT,
            anchor="w",
        ).pack(anchor="w", padx=14, pady=(14, 6))

        return card

    def fetch_entries(self):
        result = fetch_user_passwords()

        if not result["success"]:
            messagebox.showerror(
                "Backup failed",
                result.get("error", "Could not fetch vault items."),
            )
            return None

        return result["data"]

    def export_encrypted(self):
        entries = self.fetch_entries()

        if entries is None:
            return

        default_name = f"snakevault-backup-{datetime.now().strftime('%Y-%m-%d')}.svb"

        path = filedialog.asksaveasfilename(
            title="Export encrypted backup",
            defaultextension=".svb",
            initialfile=default_name,
            filetypes=[("SnakeVault Backup", "*.svb"), ("JSON files", "*.json")],
        )

        if not path:
            return

        payload = {
            "app": "SnakeVault",
            "version": 1,
            "exported_at": datetime.now().isoformat(),
            "entries": entries,
        }

        try:
            with open(path, "w", encoding="utf-8") as file:
                json.dump(payload, file, indent=2)
        except OSError as error:
            messagebox.showerror("Backup failed", str(error))
            return

        messagebox.showinfo("Backup complete", "Encrypted backup exported successfully.")

    def export_csv(self):
        confirm = messagebox.askyesno(
            "Plain text export warning",
            "CSV export decrypts your passwords into plain text.\n\nContinue only if you understand the risk.",
        )

        if not confirm:
            return

        entered_key = simpledialog.askstring(
            "Verify master key",
            "Enter your master key to export CSV:",
            show="*",
            parent=self,
        )

        if not entered_key:
            return
        
                key_result = get_master_key()

        if not key_result["success"] or not key_result["data"]:
            messagebox.showerror(
                "Verification failed",
                key_result.get("error", "Could not verify master key."),
            )
            return

        if not verify_key(entered_key, key_result["data"]):
            messagebox.showerror(
                "Wrong key",
                "Incorrect master key. CSV export cancelled.",
            )
            return

        entries = self.fetch_entries()

        if entries is None:
            return

        default_name = f"snakevault-export-{datetime.now().strftime('%Y-%m-%d')}.csv"

        path = filedialog.asksaveasfilename(
            title="Export CSV",
            defaultextension=".csv",
            initialfile=default_name,
            filetypes=[("CSV files", "*.csv")],
        )

        if not path:
            return

        try:
            with open(path, "w", encoding="utf-8", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["site_name", "url", "username", "password", "category", "notes"])

                for item in entries:
                    password = decrypt(item.get("encrypted_password", ""), entered_key)
                    writer.writerow([
                        item.get("site_name", ""),
                        item.get("url", ""),
                        item.get("username", ""),
                        password,
                        item.get("category", "General"),
                        item.get("notes", ""),
                    ])
        except Exception as error:
            messagebox.showerror("CSV export failed", str(error))
            return

        messagebox.showinfo("CSV exported", "Plain text CSV exported. Delete it when finished.")

    def import_placeholder(self):
        messagebox.showinfo(
            "Import coming soon",
            "Encrypted import can be added as a future improvement.",
        )