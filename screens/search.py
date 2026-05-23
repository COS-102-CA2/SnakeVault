import tkinter as tk
from tkinter import messagebox

from libs.db import fetch_user_passwords
from libs.window_manager import (
    BG,
    BORDER,
    FONT,
    FONT_LG,
    FONT_TITLE,
    GOLD,
    ICON_KEY,
    ICON_SEARCH,
    MUTED,
    PAD_X,
    SURFACE,
    SURFACE2,
    TEXT,
    clear_frame,
    make_button,
    make_entry,
)


class SearchScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller

        if not self.controller.master_key:
            self.after(0, lambda: self.controller.show_screen("login"))
            return
            
        self.entries = []
        self.filtered = []

        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        top = tk.Frame(self, bg=BG)
        top.grid(row=0, column=0, sticky="ew", padx=PAD_X, pady=(42, 18))
        top.columnconfigure(0, weight=1)

        tk.Label(top, text=f"{ICON_SEARCH} All Passwords", font=FONT_TITLE, fg=GOLD, bg=BG).grid(row=0, column=0, sticky="w")
        make_button(top, "Back", lambda: controller.show_screen("dashboard"), variant="secondary").grid(row=0, column=1, sticky="e", ipadx=18, ipady=7)

        search_row = tk.Frame(self, bg=BG)
        search_row.grid(row=1, column=0, sticky="ew", padx=PAD_X, pady=(0, 14))
        search_row.columnconfigure(0, weight=1)

        self.search_entry = make_entry(search_row)
        self.search_entry.grid(row=0, column=0, sticky="ew", ipady=9)
        self.search_entry.bind("<KeyRelease>", lambda _event: self.filter_entries())

        make_button(search_row, "Add", lambda: controller.show_screen("add_password")).grid(row=0, column=1, padx=(10, 0), ipadx=18, ipady=8)

        self.result_frame = tk.Frame(self, bg=SURFACE, highlightbackground=BORDER, highlightthickness=1)
        self.result_frame.grid(row=2, column=0, sticky="nsew", padx=PAD_X, pady=(0, 36))

        self.load_entries()

    def load_entries(self):
        result = fetch_user_passwords()
        if not result["success"]:
            messagebox.showerror("Error", result.get("error", "Could not fetch vault items."))
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
        clear_frame(self.result_frame)

        if not self.filtered:
            tk.Label(self.result_frame, text="No results found.", font=FONT, fg=MUTED, bg=SURFACE).pack(pady=80)
            return

        for item in self.filtered:
            row = tk.Frame(self.result_frame, bg=SURFACE)
            row.pack(fill="x", padx=18, pady=8)
            row.bind("<Button-1>", lambda _event, entry=item: self.open_detail(entry))

            tk.Label(row, text=ICON_KEY, font=FONT_LG, fg=GOLD, bg=SURFACE).pack(side="left", padx=(0, 12))

            text = tk.Frame(row, bg=SURFACE)
            text.pack(side="left", fill="x", expand=True)

            tk.Label(text, text=item.get("site_name", "Untitled"), font=FONT_LG, fg=TEXT, bg=SURFACE).pack(anchor="w")
            tk.Label(text, text=item.get("username", ""), font=FONT, fg=MUTED, bg=SURFACE).pack(anchor="w")

            tk.Label(row, text=item.get("category") or "General", font=FONT, fg=TEXT, bg=SURFACE2, padx=10, pady=4).pack(side="right")

    def open_detail(self, entry):
        self.controller.show_screen("password_detail", entry=entry)