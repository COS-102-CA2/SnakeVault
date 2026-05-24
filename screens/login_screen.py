import customtkinter as ctk
from tkinter import messagebox

from libs.db import get_master_key, login_user, sign_up_user
from libs.window_manager import (
    BG,
    FONT,
    FONT_LG,
    FONT_SM,
    FONT_TITLE,
    GOLD,
    ICON_LOCK,
    ICON_SNAKE,
    MUTED,
    SURFACE,
    SURFACE2,
    TEXT,
    make_button,
    make_card,
    make_entry,
)


class LoginScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent, fg_color=BG, corner_radius=0)
        self.controller = controller
        self.mode = "login"

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        shell = ctk.CTkFrame(self, fg_color=BG, corner_radius=0)
        shell.grid(row=0, column=0)

        ctk.CTkLabel(
            shell,
            text=f"{ICON_SNAKE} {ICON_LOCK}",
            font=("Segoe UI Emoji", 36),
            text_color=GOLD,
        ).pack(pady=(0, 18))

        ctk.CTkLabel(
            shell,
            text="SnakeVault",
            font=FONT_TITLE,
            text_color=GOLD,
        ).pack()

        ctk.CTkLabel(
            shell,
            text="Sign in or create an account to continue",
            font=FONT,
            text_color=MUTED,
        ).pack(pady=(6, 24))

        self.card = make_card(shell)
        self.card.pack(ipadx=34, ipady=28)

        self.mode_frame = ctk.CTkFrame(self.card, fg_color=SURFACE, corner_radius=0)
        self.mode_frame.pack(fill="x", pady=(0, 22), padx=0)

        self.login_tab = make_button(
            self.mode_frame,
            "Returning user",
            lambda: self.set_mode("login"),
        )
        self.login_tab.pack(side="left", fill="x", expand=True, padx=(0, 6), ipady=4)

        self.signup_tab = make_button(
            self.mode_frame,
            "New user",
            lambda: self.set_mode("signup"),
            variant="secondary",
        )
        self.signup_tab.pack(side="left", fill="x", expand=True, padx=(6, 0), ipady=4)

        ctk.CTkLabel(
            self.card,
            text="Email address",
            font=FONT,
            text_color=MUTED,
            fg_color=SURFACE,
            anchor="w",
        ).pack(fill="x")

        self.email_entry = make_entry(self.card)
        self.email_entry.pack(fill="x", pady=(6, 14), ipady=5)

        ctk.CTkLabel(
            self.card,
            text="Account password",
            font=FONT,
            text_color=MUTED,
            fg_color=SURFACE,
            anchor="w",
        ).pack(fill="x")

        self.password_entry = make_entry(self.card, show="*")
        self.password_entry.pack(fill="x", pady=(6, 8), ipady=5)

        self.status_label = ctk.CTkLabel(
            self.card,
            text="",
            font=FONT_SM,
            text_color=MUTED,
            fg_color=SURFACE,
            anchor="w",
        )
        self.status_label.pack(fill="x", pady=(2, 14))

        self.submit_btn = make_button(
            self.card,
            "Sign in",
            self.handle_submit,
            font=FONT_LG,
        )
        self.submit_btn.pack(fill="x", ipady=5)

        ctk.CTkLabel(
            shell,
            text="Your master key is requested only after account authentication.",
            font=FONT_SM,
            text_color=MUTED,
        ).pack(pady=(14, 0))

        self.set_mode("login")

    def set_mode(self, mode):
        self.mode = mode
        is_login = mode == "login"

        self.login_tab.configure(
            fg_color=GOLD if is_login else SURFACE2,
            text_color="#161622" if is_login else TEXT,
        )
        self.signup_tab.configure(
            fg_color=GOLD if not is_login else SURFACE2,
            text_color="#161622" if not is_login else TEXT,
        )
        self.submit_btn.configure(text="Sign in" if is_login else "Create account")
        self.status_label.configure(
            text=(
                "Returning users continue to master key verification."
                if is_login
                else "New users create a master key after account setup."
            )
        )

    def handle_submit(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showwarning(
                "Missing details",
                "Please enter both email and account password.",
            )
            return

        if self.mode == "signup":
            self.handle_signup(email, password)
        else:
            self.handle_login(email, password)

    def handle_login(self, email, password):
        result = login_user(email, password)

        if not result["success"]:
            messagebox.showerror(
                "Login failed",
                result.get("error", "Invalid credentials."),
            )
            return

        key_result = get_master_key()

        if not key_result["success"]:
            messagebox.showerror(
                "Vault check failed",
                key_result.get("error", "Could not check your vault."),
            )
            return

        if key_result["data"]:
            self.controller.show_screen("unlock")
        else:
            self.controller.show_screen("create_key")

    def handle_signup(self, email, password):
        result = sign_up_user(email, password)

        if not result["success"]:
            messagebox.showerror(
                "Sign up failed",
                result.get("error", "Could not register user."),
            )
            return

        login_result = login_user(email, password)

        if login_result["success"]:
            self.controller.show_screen("create_key")
        else:
            messagebox.showinfo(
                "Account created",
                "Account created. Please sign in, then create your master key.",
            )
            self.set_mode("login")