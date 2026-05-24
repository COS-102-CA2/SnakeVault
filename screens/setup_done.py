import customtkinter as ctk

from libs.window_manager import BG, FONT, FONT_LG, FONT_TITLE, GOLD, ICON_LOCK, MUTED, SUCCESS, make_button


class SetupDoneScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.controller = controller

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        content = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        content.grid(row=0, column=0)

        ctk.CTkLabel(
            content,
            text=ICON_LOCK,
            font=("Segoe UI Emoji", 46),
            text_color=GOLD,
        ).pack(pady=(0, 22))

        ctk.CTkLabel(
            content,
            text="Vault Setup Complete",
            font=FONT_TITLE,
            text_color=GOLD,
        ).pack()

        ctk.CTkLabel(
            content,
            text="Your master key is ready for this session.",
            font=FONT,
            text_color=MUTED,
        ).pack(pady=(8, 10))

        ctk.CTkLabel(
            content,
            text="Keep it somewhere safe offline.",
            font=FONT,
            text_color=SUCCESS,
        ).pack(pady=(0, 42))

        make_button(
            content,
            "Enter dashboard",
            lambda: controller.show_screen("dashboard"),
            font=FONT_LG,
        ).pack(ipadx=30, ipady=8)

        make_button(
            content,
            "Back to sign in",
            lambda: controller.show_screen("login"),
            variant="secondary",
        ).pack(pady=14, ipadx=22, ipady=6)