import customtkinter as ctk

from libs.window_manager import (
    BG,
    FONT,
    FONT_DISPLAY,
    FONT_LG,
    GOLD,
    ICON_KEY,
    ICON_LOCK,
    ICON_SNAKE,
    MUTED,
    make_button,
)


class WelcomeScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        content = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        content.grid(row=0, column=0)

        ctk.CTkLabel(
            content,
            text=f"{ICON_SNAKE}  {ICON_LOCK}",
            font=("Segoe UI Emoji", 42),
            text_color=GOLD,
        ).pack(pady=(0, 24))

        ctk.CTkLabel(
            content,
            text="SnakeVault",
            font=FONT_DISPLAY,
            text_color=GOLD,
        ).pack()

        ctk.CTkLabel(
            content,
            text="Your secure password manager",
            font=FONT,
            text_color=MUTED,
        ).pack(pady=(8, 54))

        actions = ctk.CTkFrame(content, fg_color=BG, corner_radius=0)
        actions.pack()

        make_button(
            actions,
            f"{ICON_KEY} Create new vault",
            lambda: controller.show_screen("login"),
            font=FONT_LG,
        ).pack(side="left", padx=10, ipadx=14, ipady=8)

        make_button(
            actions,
            f"{ICON_LOCK} Unlock existing vault",
            lambda: controller.show_screen("login"),
            variant="secondary",
            font=FONT_LG,
        ).pack(side="left", padx=10, ipadx=14, ipady=8)

        ctk.CTkLabel(
            content,
            text="AES encrypted · Zero knowledge · On-device master key",
            font=FONT,
            text_color=MUTED,
        ).pack(pady=(36, 0))