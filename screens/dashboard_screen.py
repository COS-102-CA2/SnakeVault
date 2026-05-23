import tkinter as tk
from tkinter import messagebox

from libs.db import fetch_user_passwords, logout_user
from libs.window_manager import (
    BG,
    BORDER,
    FONT,
    FONT_LG,
    FONT_TITLE,
    GOLD,
    ICON_CLOCK,
    ICON_FOLDER,
    ICON_GENERATOR,
    ICON_KEY,
    ICON_LOCK,
    ICON_SEARCH,
    ICON_SETTINGS,
    ICON_SNAKE,
    MUTED,
    PAD_X,
    SURFACE,
    SURFACE2,
    TEXT,
    clear_frame,
    make_button,
)


class DashboardScreen(tk.Frame):
    def _init_(self, parent, controller):
        super()._init_(parent, bg=BG)
        self.controller = controller
        self.entries = []

        if not self.controller.master_key:
            self.after(0, lambda: self.controller.show_screen("login"))
            return

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self.sidebar = tk.Frame(self, bg="#151522", width=172)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        self.main = tk.Frame(self, bg=BG)
        self.main.grid(row=0, column=1, sticky="nsew", padx=18, pady=16)
        self.main.columnconfigure(0, weight=1)
        self.main.rowconfigure(3, weight=1)

        self.build_sidebar()
        self.build_main()
        self.load_vault_data()

    def build_sidebar(self):
        tk.Label(
            self.sidebar,
            text=f"{ICON_SNAKE} SnakeVault",
            font=FONT_LG,
            fg=GOLD,
            bg="#151522",
        ).pack(anchor="w", padx=16, pady=(24, 2))

        self.entry_count = tk.Label(
            self.sidebar,
            text="0 entries",
            font=FONT,
            fg=MUTED,
            bg="#151522",
        )
        self.entry_count.pack(anchor="w", padx=16, pady=(0, 24))

        nav_items = [
            ("▦  Dashboard", "dashboard"),
            (f"{ICON_KEY}  Passwords", "search"),
            (f"{ICON_SEARCH}  Search", "search"),
            (f"{ICON_GENERATOR}  Generator", "generator"),
            (f"{ICON_SETTINGS}  Settings", "settings"),
        ]

        for text, target in nav_items:
            active = target == "dashboard"

            tk.Button(
                self.sidebar,
                text=text,
                font=FONT,
                anchor="w",
                bg=SURFACE if active else "#151522",
                fg=GOLD if active else MUTED,
                activebackground=SURFACE,
                activeforeground=TEXT,
                bd=0,
                command=lambda screen=target: self.controller.show_screen(screen),
            ).pack(fill="x", padx=0, pady=2, ipady=9)

        tk.Button(
            self.sidebar,
            text=f"{ICON_LOCK}  Lock",
            font=FONT,
            bg="#E06B6B",
            fg="#11111b",
            bd=0,
            command=self.handle_logout,
        ).pack(side="bottom", anchor="w", padx=14, pady=22, ipadx=22, ipady=8)

    def build_main(self):
        tk.Label(
            self.main,
            text="Dashboard",
            font=FONT_TITLE,
            fg=GOLD,
            bg=BG,
        ).grid(row=0, column=0, sticky="w")

        tk.Label(
            self.main,
            text="Your saved credentials at a glance",
            font=FONT,
            fg=MUTED,
            bg=BG,
        ).grid(row=1, column=0, sticky="w", pady=(2, 16))

        stats = tk.Frame(self.main, bg=BG)
        stats.grid(row=2, column=0, sticky="ew")
        stats.columnconfigure(0, weight=1)
        stats.columnconfigure(1, weight=1)
        stats.columnconfigure(2, weight=1)
        stats.columnconfigure(3, weight=1)

        self.total_value = self.stat_card(stats, 0, ICON_KEY, "0", "Total")
        self.weak_value = self.stat_card(stats, 1, "⚠️", "0", "Weak")
        self.category_value = self.stat_card(stats, 2, ICON_FOLDER, "0", "Categories")
        self.updated_value = self.stat_card(stats, 3, ICON_CLOCK, "Today", "Updated")

        header = tk.Frame(self.main, bg=BG)
        header.grid(row=3, column=0, sticky="nsew", pady=(18, 0))
        header.columnconfigure(0, weight=1)
        header.rowconfigure(1, weight=1)

        top_line = tk.Frame(header, bg=BG)
        top_line.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        top_line.columnconfigure(0, weight=1)

        tk.Label(
            top_line,
            text="Recently accessed",
            font=FONT_LG,
            fg=TEXT,
            bg=BG,
        ).grid(row=0, column=0, sticky="w")

        make_button(
            top_line,
            "Refresh",
            self.load_vault_data,
            variant="secondary",
        ).grid(row=0, column=1, sticky="e", ipadx=14, ipady=6)

        self.list_frame = tk.Frame(
            header,
            bg=SURFACE,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        self.list_frame.grid(row=1, column=0, sticky="nsew")

        footer = tk.Frame(self.main, bg=BG)
        footer.grid(row=4, column=0, sticky="ew", pady=(12, 0))
        footer.columnconfigure(0, weight=1)

        make_button(
            footer,
            "View all →",
            lambda: self.controller.show_screen("search"),
            variant="secondary",
        ).grid(row=0, column=1, ipadx=24, ipady=8, padx=(0, 10))

        make_button(
            footer,
            "+ Add password",
            lambda: self.controller.show_screen("add_password"),
            variant="primary",
            font=FONT_LG,
        ).grid(row=0, column=2, ipadx=28, ipady=8)

    def stat_card(self, parent, column, icon, value, label):
        card = tk.Frame(
            parent,
            bg=SURFACE,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        card.grid(row=0, column=column, sticky="ew", padx=(0, 10), ipady=10)

        tk.Label(
            card,
            text=icon,
            font=FONT_LG,
            fg=GOLD,
            bg=SURFACE,
        ).pack()

        value_label = tk.Label(
            card,
            text=value,
            font=FONT_LG,
            fg=GOLD,
            bg=SURFACE,
        )
        value_label.pack()

        tk.Label(
            card,
            text=label,
            font=FONT,
            fg=MUTED,
            bg=SURFACE,
        ).pack()

        return value_label

    def load_vault_data(self):
        clear_frame(self.list_frame)

        result = fetch_user_passwords()

        if not result["success"]:
            messagebox.showerror(
                "Error",
                result.get("error", "Could not fetch vault items."),
            )
            return

        self.entries = result["data"]

        total = len(self.entries)
        categories = {
            item.get("category") or "General"
            for item in self.entries
        }
        weak = sum(
            1
            for item in self.entries
            if "weak" in (item.get("notes") or "").lower()
        )

        self.total_value.configure(text=str(total))
        self.weak_value.configure(text=str(weak))
        self.category_value.configure(text=str(len(categories)))
        self.entry_count.configure(text=f"{total} entries")

        if not self.entries:
            tk.Label(
                self.list_frame,
                text="No passwords yet.",
                font=FONT,
                fg=MUTED,
                bg=SURFACE,
            ).pack(pady=80)
            return

        for item in self.entries[:8]:
            self.add_entry_row(item)

    def add_entry_row(self, item):
        row = tk.Frame(self.list_frame, bg=SURFACE)
        row.pack(fill="x", padx=18, pady=8)

        row.bind(
            "<Button-1>",
            lambda _event: self.open_detail(item),
        )

        icon = tk.Label(
            row,
            text=ICON_KEY,
            font=FONT_LG,
            fg=GOLD,
            bg=SURFACE,
        )
        icon.pack(side="left", padx=(0, 12))

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

        category = item.get("category") or "General"

        tk.Label(
            row,
            text=category,
            font=FONT,
            fg=TEXT,
            bg=SURFACE2,
            padx=10,
            pady=4,
        ).pack(side="right")

    def open_detail(self, entry):
        self.controller.show_screen("password_detail", entry=entry)

    def handle_logout(self):
        logout_user()
        self.controller.master_key = None
        self.controller.show_screen("login")