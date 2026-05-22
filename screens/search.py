import tkinter as tk
from tkinter import messagebox

from db import fetch_user_passwords
from libs.window_manager import BG, BORDER, GOLD, MUTED, SURFACE, SURFACE2, TEXT, FONT, FONT_LG, FONT_TITLE


class SearchScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.entries = []
        self.filtered = []

        top = tk.Frame(self, bg=BG)
        top.pack(fill="x", padx=54, pady=(42, 18))

        tk.Label(
            top,
            text="All Passwords",
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

        search_row = tk.Frame(self, bg=BG)
        search_row.pack(fill="x", padx=54, pady=(0, 14))

        self.search_entry = tk.Entry(
            search_row,
            font=FONT,
            bg=SURFACE2,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
        )
        self.search_entry.pack(side="left", fill="x", expand=True, ipady=9)

        self.search_entry.bind(
            "<KeyRelease>",
            lambda _event: self.filter_entries(),
        )

        tk.Button(
            search_row,
            text="Add",
            font=FONT,
            bg=GOLD,
            fg="#161622",
            bd=0,
            command=lambda: controller.show_screen("add_password"),
        ).pack(side="left", padx=(10, 0), ipadx=18, ipady=8)

        self.result_frame = tk.Frame(
            self,
            bg=SURFACE,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        self.result_frame.pack(fill="both", expand=True, padx=54, pady=(0, 36))

        self.load_entries()

    def load_entries(self):
        result = fetch_user_passwords()

        if not result["success"]:
            messagebox.showerror(
                "Error",
                result.get("error", "Could not fetch vault items."),
            )
            return

        self.entries = result["data"]
        self.filter_entries()

    def filter_entries(self):
        query = self.search_entry.get().strip().lower()

        self.filtered = [
            item
            for item in self.entries
            if query in (item.get("site_name") or "").lower()
            or query in (item.get("username") or "").lower()
            or query in (item.get("category") or "").lower()
        ]

        self.render_results()

    def render_results(self):
        for child in self.result_frame.winfo_children():
            child.destroy()

        for item in self.filtered:
            row = tk.Frame(self.result_frame, bg=SURFACE)
            row.pack(fill="x", padx=18, pady=8)

            row.bind(
                "<Button-1>",
                lambda _event, entry=item: self.open_detail(entry),
            )

            text = tk.Frame(row, bg=SURFACE)
            text.pack(side="left", fill="x", expand=True)

            tk.Label(
                text,
                text=item.get("site_name", "Untitled"),
                font=FONT_LG,
                fg=TEXT,
                bg=SURFACE,
            ).pack(anchor="w")

            tk.Label(
                text,
                text=item.get("username", ""),
                font=FONT,
                fg=MUTED,
                bg=SURFACE,
            ).pack(anchor="w")

            tk.Label(
                row,
                text=item.get("category") or "General",
                font=FONT,
                fg=TEXT,
                bg=SURFACE2,
                padx=10,
                pady=4,
            ).pack(side="right")

    def open_detail(self, entry):
        self.controller.show_screen("password_detail", entry=entry)