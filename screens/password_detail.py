import tkinter as tk

from libs.window_manager import BG, BORDER, GOLD, MUTED, SURFACE, SURFACE2, TEXT, FONT, FONT_LG, FONT_TITLE


class PasswordDetailScreen(tk.Frame):
    def __init__(self, parent, controller, entry):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.entry_data = entry

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

        self.add_display(body, "Site", entry.get("site_name", ""))
        self.add_display(body, "URL", entry.get("url", ""))
        self.add_display(body, "Username", entry.get("username", ""))
        self.add_display(body, "Password", "Hidden until verified")
        self.add_display(body, "Category", entry.get("category", "General"))
        self.add_display(body, "Notes", entry.get("notes", ""))

    def add_display(self, parent, label, value):
        tk.Label(
            parent,
            text=label,
            font=FONT,
            fg=MUTED,
            bg=SURFACE,
            anchor="w",
        ).pack(fill="x")

        value_label = tk.Label(
            parent,
            text=value or "-",
            font=FONT_LG,
            fg=TEXT,
            bg=SURFACE2,
            anchor="w",
            padx=12,
            pady=8,
        )
        value_label.pack(fill="x", pady=(5, 12))

        return value_label