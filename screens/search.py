import customtkinter as ctk
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
    ScrollableFrame,
    clear_frame,
    make_button,
    make_entry,
)


class SearchScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.controller = controller
        self.entries = []
        self.filtered = []

        if not self.controller.master_key:
            self.after(0, lambda: self.controller.show_screen("login"))
            return

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        self.build_header()
        self.build_search()
        self.build_results()
        self.load_entries()

    def build_header(self):
        top = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        top.grid(row=0, column=0, sticky="ew", padx=PAD_X, pady=(42, 18))
        top.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            top,
            text=f"{ICON_SEARCH} All Passwords",
            font=FONT_TITLE,
            text_color=GOLD,
        ).grid(row=0, column=0, sticky="w")

        make_button(
            top,
            "Back",
            lambda: self.controller.show_screen("dashboard"),
            variant="secondary",
        ).grid(row=0, column=1, sticky="e", ipadx=18, ipady=7)

    def build_search(self):
        search_row = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        search_row.grid(row=1, column=0, sticky="ew", padx=PAD_X, pady=(0, 14))
        search_row.grid_columnconfigure(0, weight=1)

        self.search_entry = make_entry(search_row)
        self.search_entry.grid(row=0, column=0, sticky="ew", ipady=5)
        self.search_entry.bind("<KeyRelease>", lambda _event: self.filter_entries())

        make_button(
            search_row,
            "Add",
            lambda: self.controller.show_screen("add_password"),
        ).grid(row=0, column=1, padx=(10, 0), ipadx=18, ipady=6)

    def build_results(self):
        self.scroll = ScrollableFrame(self, fg_color=BG)
        self.scroll.grid(row=2, column=0, sticky="nsew", padx=PAD_X, pady=(0, 36))
        self.scroll.content.grid_columnconfigure(0, weight=1)

        self.result_frame = ctk.CTkFrame(
            self.scroll.content,
            fg_color=SURFACE,
            border_color=BORDER,
            border_width=1,
            corner_radius=8,
        )
        self.result_frame.grid(row=0, column=0, sticky="ew")
        self.result_frame.grid_columnconfigure(0, weight=1)

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
        clear_frame(self.result_frame)

        if not self.filtered:
            ctk.CTkLabel(
                self.result_frame,
                text="No results found.",
                font=FONT,
                text_color=MUTED,
            ).grid(row=0, column=0, pady=80)
            return

        for row_index, item in enumerate(self.filtered):
            row = ctk.CTkFrame(
                self.result_frame,
                fg_color=SURFACE,
                corner_radius=6,
            )
            row.grid(row=row_index, column=0, sticky="ew", padx=18, pady=8)
            row.grid_columnconfigure(1, weight=1)

            row.bind("<Button-1>", lambda _event, entry=item: self.open_detail(entry))
            row.bind("<Enter>", lambda _event, frame=row: frame.configure(fg_color=SURFACE2))
            row.bind("<Leave>", lambda _event, frame=row: frame.configure(fg_color=SURFACE))

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
                widget.bind("<Button-1>", lambda _event, entry=item: self.open_detail(entry))

    def open_detail(self, entry):
        self.controller.show_screen("password_detail", entry=entry)