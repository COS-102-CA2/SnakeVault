import tkinter as tk
from tkinter import messagebox

from libs.db import fetch_user_passwords, logout_user
from libs.window_manager import BG, BORDER, GOLD, MUTED, SURFACE, SURFACE2, TEXT, FONT, FONT_LG, FONT_TITLE


class DashboardScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.entries = []
        if not self.controller.master_key:
            self.after(0, lambda: self.controller.show_screen("login"))
            return

        self.sidebar = tk.Frame(self, bg="#151522", width=172)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.build_sidebar()

        self.main = tk.Frame(self, bg=BG)
        self.main.pack(side="left", fill="both", expand=True, padx=18, pady=16)

        tk.Label(
            self.main,
            text="Dashboard",
            font=FONT_TITLE,
            fg=GOLD,
            bg=BG,
        ).pack(anchor="w")

        tk.Label(
            self.main,
            text="Your saved credentials at a glance",
            font=FONT,
            fg=MUTED,
            bg=BG,
        ).pack(anchor="w", pady=(2, 16))

        stats = tk.Frame(self.main, bg=BG)
        stats.pack(fill="x")

        self.total_value = self.stat_card(stats, "0", "Total")
        self.weak_value = self.stat_card(stats, "0", "Weak")
        self.category_value = self.stat_card(stats, "0", "Categories")

        header = tk.Frame(self.main, bg=BG)
        header.pack(fill="x", pady=(18, 8))

        tk.Label(
            header,
            text="Recently accessed",
            font=FONT_LG,
            fg=TEXT,
            bg=BG,
        ).pack(side="left")

        tk.Button(
            header,
            text="Refresh",
            font=FONT,
            bg=SURFACE2,
            fg=TEXT,
            bd=0,
            command=self.load_vault_data,
        ).pack(side="right", ipadx=14, ipady=6)

        self.list_frame = tk.Frame(
            self.main,
            bg=SURFACE,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        self.list_frame.pack(fill="both", expand=True)

        footer = tk.Frame(self.main, bg=BG)
        footer.pack(fill="x", pady=(12, 0))

        tk.Button(
            footer,
            text="View all",
            font=FONT,
            bg=SURFACE2,
            fg=TEXT,
            bd=0,
            command=lambda: controller.show_screen("search"),
        ).pack(side="right", ipadx=24, ipady=8)

        tk.Button(
            footer,
            text="Add password",
            font=FONT_LG,
            bg=GOLD,
            fg="#161622",
            bd=0,
            command=lambda: controller.show_screen("add_password"),
        ).pack(side="right", padx=(0, 10), ipadx=28, ipady=8)

        self.load_vault_data()

    def build_sidebar(self):
        tk.Label(
            self.sidebar,
            text="SnakeVault",
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
            ("Dashboard", "dashboard"),
            ("Passwords", "search"),
            ("Search", "search"),
            ("Generator", "generator"),
            ("Settings", "settings"),
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
            text="Lock",
            font=FONT,
            bg="#E06B6B",
            fg="#11111b",
            bd=0,
            command=self.handle_logout,
        ).pack(side="bottom", anchor="w", padx=14, pady=22, ipadx=22, ipady=8)

    def stat_card(self, parent, value, label):
        card = tk.Frame(
            parent,
            bg=SURFACE,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        card.pack(side="left", fill="x", expand=True, padx=(0, 10), ipady=12)

        value_label = tk.Label(
            card,
            text=value,
            font=FONT_TITLE,
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
        for child in self.list_frame.winfo_children():
            child.destroy()

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