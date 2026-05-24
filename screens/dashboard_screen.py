import customtkinter as ctk
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
    ICON_REFRESH,
    ICON_SEARCH,
    ICON_SETTINGS,
    ICON_SNAKE,
    MUTED,
    PAD_X,
    SURFACE,
    SURFACE2,
    TEXT,
    ScrollableFrame,
    clear_frame,
    make_button,
)


class DashboardScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.controller = controller
        self.entries = []

        if not self.controller.master_key:
            self.after(0, lambda: self.controller.show_screen("login"))
            return

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, fg_color="#151522", corner_radius=0, width=172)
        self.sidebar.grid(row=0, column=0, sticky="ns")
        self.sidebar.grid_propagate(False)

        self.main = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        self.main.grid(row=0, column=1, sticky="nsew", padx=18, pady=16)
        self.main.grid_columnconfigure(0, weight=1)
        self.main.grid_rowconfigure(3, weight=1)

        self.build_sidebar()
        self.build_main()
        self.load_vault_data()

    def build_sidebar(self):
        ctk.CTkLabel(
            self.sidebar,
            text=f"{ICON_SNAKE} SnakeVault",
            font=FONT_LG,
            text_color=GOLD,
        ).pack(anchor="w", padx=16, pady=(24, 2))

        self.entry_count = ctk.CTkLabel(
            self.sidebar,
            text="0 entries",
            font=FONT,
            text_color=MUTED,
        )
        self.entry_count.pack(anchor="w", padx=16, pady=(0, 24))

        nav_items = [
            ("▦  Dashboard", "dashboard"),
            (f"{ICON_SEARCH}  Search", "search"),
            (f"{ICON_GENERATOR}  Generator", "generator"),
            (f"{ICON_SETTINGS}  Settings", "settings"),
        ]

        for text, target in nav_items:
            active = target == "dashboard"

            ctk.CTkButton(
                self.sidebar,
                text=text,
                font=FONT,
                anchor="w",
                fg_color=SURFACE if active else "#151522",
                text_color=GOLD if active else MUTED,
                hover_color=SURFACE,
                corner_radius=0,
                command=lambda screen=target: self.controller.show_screen(screen),
            ).pack(fill="x", padx=0, pady=2, ipady=4)

        make_button(
            self.sidebar,
            f"{ICON_LOCK}  Lock",
            self.handle_logout,
            variant="danger",
        ).pack(side="bottom", anchor="w", padx=14, pady=22, ipadx=12, ipady=5)

    def build_main(self):
        ctk.CTkLabel(
            self.main,
            text="Dashboard",
            font=FONT_TITLE,
            text_color=GOLD,
        ).grid(row=0, column=0, sticky="w")

        ctk.CTkLabel(
            self.main,
            text="Your saved credentials at a glance",
            font=FONT,
            text_color=MUTED,
        ).grid(row=1, column=0, sticky="w", pady=(2, 16))

        stats = ctk.CTkFrame(self.main, fg_color=BG, corner_radius=0)
        stats.grid(row=2, column=0, sticky="ew")
        for index in range(4):
            stats.grid_columnconfigure(index, weight=1)

        self.total_value = self.stat_card(stats, 0, ICON_KEY, "0", "Total")
        self.protected_value = self.stat_card(stats, 1, ICON_LOCK, "0", "Protected")
        self.category_value = self.stat_card(stats, 2, ICON_FOLDER, "0", "Categories")
        self.updated_value = self.stat_card(stats, 3, ICON_CLOCK, "Today", "Updated")

        header = ctk.CTkFrame(self.main, fg_color=BG, corner_radius=0)
        header.grid(row=3, column=0, sticky="nsew", pady=(18, 0))
        header.grid_columnconfigure(0, weight=1)
        header.grid_rowconfigure(1, weight=1)

        top_line = ctk.CTkFrame(header, fg_color=BG, corner_radius=0)
        top_line.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        top_line.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            top_line,
            text="Recently accessed",
            font=FONT_LG,
            text_color=TEXT,
        ).grid(row=0, column=0, sticky="w")

        make_button(
            top_line,
            f"{ICON_REFRESH} Refresh",
            self.load_vault_data,
            variant="secondary",
        ).grid(row=0, column=1, sticky="e", ipadx=10, ipady=4)

        self.scroll = ScrollableFrame(header, fg_color=SURFACE)
        self.scroll.grid(row=1, column=0, sticky="nsew")
        self.scroll.content.grid_columnconfigure(0, weight=1)

        self.list_frame = ctk.CTkFrame(
            self.scroll.content,
            fg_color=SURFACE,
            border_color=BORDER,
            border_width=1,
            corner_radius=8,
        )
        self.list_frame.grid(row=0, column=0, sticky="ew")
        self.list_frame.grid_columnconfigure(0, weight=1)

        footer = ctk.CTkFrame(self.main, fg_color=BG, corner_radius=0)
        footer.grid(row=4, column=0, sticky="ew", pady=(12, 0))
        footer.grid_columnconfigure(0, weight=1)

        make_button(
            footer,
            "View all →",
            lambda: self.controller.show_screen("search"),
            variant="secondary",
        ).grid(row=0, column=1, ipadx=18, ipady=6, padx=(0, 10))

        make_button(
            footer,
            "+ Add password",
            lambda: self.controller.show_screen("add_password"),
            variant="primary",
            font=FONT_LG,
        ).grid(row=0, column=2, ipadx=22, ipady=6)

    def stat_card(self, parent, column, icon, value, label):
        card = ctk.CTkFrame(
            parent,
            fg_color=SURFACE,
            border_color=BORDER,
            border_width=1,
            corner_radius=8,
        )
        card.grid(row=0, column=column, sticky="ew", padx=(0, 10), ipady=10)

        ctk.CTkLabel(card, text=icon, font=FONT_LG, text_color=GOLD).pack()
        value_label = ctk.CTkLabel(card, text=value, font=FONT_LG, text_color=GOLD)
        value_label.pack()
        ctk.CTkLabel(card, text=label, font=FONT, text_color=MUTED).pack()

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

        self.total_value.configure(text=str(total))
        self.protected_value.configure(text=str(total))
        self.category_value.configure(text=str(len(categories)))
        self.entry_count.configure(text=f"{total} entries")

        if not self.entries:
            ctk.CTkLabel(
                self.list_frame,
                text="No passwords yet.",
                font=FONT,
                text_color=MUTED,
            ).grid(row=0, column=0, pady=80)
            return

        for row_index, item in enumerate(self.entries):
            self.add_entry_row(item, row_index)

    def add_entry_row(self, item, row_index):
        row = ctk.CTkFrame(
            self.list_frame,
            fg_color=SURFACE,
            corner_radius=6,
        )
        row.grid(row=row_index, column=0, sticky="ew", padx=18, pady=8)
        row.grid_columnconfigure(1, weight=1)

        row.bind("<Button-1>", lambda _event: self.open_detail(item))
        row.bind("<Enter>", lambda _event: row.configure(fg_color=SURFACE2))
        row.bind("<Leave>", lambda _event: row.configure(fg_color=SURFACE))

        icon = ctk.CTkLabel(
            row,
            text=ICON_KEY,
            font=FONT_LG,
            text_color=GOLD,
        )
        icon.grid(row=0, column=0, rowspan=2, padx=(0, 12), sticky="w")

        site_label = ctk.CTkLabel(
            row,
            text=item.get("site_name", "Untitled"),
            font=FONT_LG,
            text_color=TEXT,
        )
        site_label.grid(row=0, column=1, sticky="w")

        user_label = ctk.CTkLabel(
            row,
            text=item.get("username", ""),
            font=FONT,
            text_color=MUTED,
        )
        user_label.grid(row=1, column=1, sticky="w")

        category_label = ctk.CTkLabel(
            row,
            text=item.get("category") or "General",
            font=FONT,
            text_color=TEXT,
            fg_color=SURFACE2,
            corner_radius=5,
        )
        category_label.grid(row=0, column=2, rowspan=2, sticky="e", padx=10, pady=4)

        for widget in (icon, site_label, user_label, category_label):
            widget.bind("<Button-1>", lambda _event: self.open_detail(item))

    def open_detail(self, entry):
        self.controller.show_screen("password_detail", entry=entry)

    def handle_logout(self):
        logout_user()
        self.controller.master_key = None
        self.controller.show_screen("login")