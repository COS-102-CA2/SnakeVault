import customtkinter as ctk
from tkinter import messagebox

from libs.db import save_master_key
from libs.crypto import hash_key
from libs.window_manager import (
    BG,
    DANGER,
    FONT,
    FONT_LG,
    FONT_TITLE,
    GOLD,
    ICON_KEY,
    MUTED,
    PAD_X,
    SUCCESS,
    SURFACE,
    make_button,
    make_card,
    make_entry,
    make_field_label,
)


class ConfirmKeyScreen(ctk.CTkFrame):
    def __init__(self, parent, controller, master_key):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.controller = controller
        self.master_key = master_key

        self.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            self,
            text=f"{ICON_KEY} Confirm Your Master Key",
            font=FONT_TITLE,
            text_color=GOLD,
        ).grid(row=0, column=0, pady=(72, 8))

        ctk.CTkLabel(
            self,
            text="Re-enter your passphrase exactly",
            font=FONT,
            text_color=MUTED,
        ).grid(row=1, column=0)

        card = make_card(self)
        card.grid(row=2, column=0, sticky="ew", padx=PAD_X, pady=28)
        card.grid_columnconfigure(0, weight=1)

        make_field_label(card, "Master key again").grid(row=0, column=0, sticky="ew", padx=18, pady=(18, 6))

        self.confirm_entry = make_entry(card, show="*")
        self.confirm_entry.grid(row=1, column=0, sticky="ew", padx=18, ipady=5)
        self.confirm_entry.bind("<KeyRelease>", self.update_match_state)

        self.match_label = ctk.CTkLabel(
            card,
            text="",
            font=FONT,
            text_color=MUTED,
            fg_color=SURFACE,
            anchor="w",
        )
        self.match_label.grid(row=2, column=0, sticky="ew", padx=18, pady=(12, 18))

        actions = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        actions.grid(row=3, column=0, sticky="e", padx=PAD_X, pady=(70, 0))

        make_button(actions, "Create vault →", self.create_vault, font=FONT_LG).pack(side="right", ipadx=20, ipady=6)
        make_button(actions, "Cancel", self.cancel, variant="secondary").pack(side="right", padx=(0, 12), ipadx=18, ipady=6)
        make_button(actions, "← Back", self.go_back, variant="secondary").pack(side="right", padx=(0, 12), ipadx=18, ipady=6)

        self.confirm_entry.focus_set()

    def update_match_state(self, _event=None):
        value = self.confirm_entry.get()

        if not value:
            self.match_label.configure(text="", text_color=MUTED)
        elif value == self.master_key:
            self.match_label.configure(text="Keys match. You are good to go.", text_color=SUCCESS)
        else:
            self.match_label.configure(text="Keys do not match. Clear and try again.", text_color=DANGER)

    def create_vault(self):
        if self.confirm_entry.get() != self.master_key:
            messagebox.showwarning(
                "Keys do not match",
                "Re-enter the same master key to continue.",
            )
            self.confirm_entry.delete(0, "end")
            self.update_match_state()
            return

        result = save_master_key(hash_key(self.master_key))

        if not result["success"]:
            messagebox.showerror(
                "Could not save master key",
                result.get("error", "Please try again."),
            )
            return

        self.controller.master_key = self.master_key
        self.master_key = None
        self.controller.show_screen("setup_done")

    def go_back(self):
        self.controller.show_screen("create_key")

    def cancel(self):
        self.master_key = None
        self.controller.master_key = None
        self.controller.show_screen("login")