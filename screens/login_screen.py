import tkinter as tk
from tkinter import messagebox

from db import get_master_key, login_user, sign_up_user
from libs.window_manager import BG, BORDER, GOLD, MUTED, SURFACE, SURFACE2, TEXT, FONT, FONT_LG, FONT_SM, FONT_TITLE


class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG)
        self.controller = controller
        self.mode = "login"

        shell = tk.Frame(self, bg=BG)
        shell.pack(fill="both", expand=True, padx=54, pady=42)

        tk.Label(
            shell,
            text="SnakeVault",
            font=FONT_TITLE,
            fg=GOLD,
            bg=BG,
        ).pack(pady=(28, 6))

        tk.Label(
            shell,
            text="Sign in or create an account to continue to your vault",
            font=FONT,
            fg=MUTED,
            bg=BG,
        ).pack()

        self.card = tk.Frame(
            shell,
            bg=SURFACE,
            highlightbackground=BORDER,
            highlightthickness=1,
        )
        self.card.pack(pady=32, ipadx=34, ipady=28)

        self.mode_frame = tk.Frame(self.card, bg=SURFACE)
        self.mode_frame.pack(fill="x", pady=(0, 22))

        self.login_tab = tk.Button(
            self.mode_frame,
            text="Returning user",
            font=FONT,
            bd=0,
            command=lambda: self.set_mode("login"),
        )
        self.login_tab.pack(side="left", fill="x", expand=True, padx=(0, 6), ipady=8)

        self.signup_tab = tk.Button(
            self.mode_frame,
            text="New user",
            font=FONT,
            bd=0,
            command=lambda: self.set_mode("signup"),
        )
        self.signup_tab.pack(side="left", fill="x", expand=True, padx=(6, 0), ipady=8)

        tk.Label(
            self.card,
            text="Email address",
            font=FONT,
            fg=MUTED,
            bg=SURFACE,
            anchor="w",
        ).pack(fill="x")

        self.email_entry = self.make_entry(self.card)
        self.email_entry.pack(fill="x", pady=(6, 14), ipady=8)

        tk.Label(
            self.card,
            text="Account password",
            font=FONT,
            fg=MUTED,
            bg=SURFACE,
            anchor="w",
        ).pack(fill="x")

        self.password_entry = self.make_entry(self.card, show="*")
        self.password_entry.pack(fill="x", pady=(6, 8), ipady=8)

        self.status_label = tk.Label(
            self.card,
            text="",
            font=FONT_SM,
            fg=MUTED,
            bg=SURFACE,
            anchor="w",
        )
        self.status_label.pack(fill="x", pady=(2, 14))

        self.submit_btn = tk.Button(
            self.card,
            text="Sign in",
            font=FONT_LG,
            bg=GOLD,
            fg="#161622",
            activebackground="#D8BA5C",
            activeforeground="#161622",
            bd=0,
            command=self.handle_submit,
        )
        self.submit_btn.pack(fill="x", ipady=9)

        tk.Label(
            shell,
            text="Your master key is requested only after your account is authenticated.",
            font=FONT_SM,
            fg=MUTED,
            bg=BG,
        ).pack(pady=(0, 8))

        self.set_mode("login")

    def make_entry(self, parent, show=None):
        return tk.Entry(
            parent,
            font=FONT,
            width=42,
            bg=SURFACE2,
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat",
            show=show,
        )

    def set_mode(self, mode):
        self.mode = mode
        is_login = mode == "login"

        self.login_tab.configure(
            bg=GOLD if is_login else SURFACE2,
            fg="#161622" if is_login else TEXT,
            activebackground=GOLD if is_login else SURFACE2,
        )

        self.signup_tab.configure(
            bg=GOLD if not is_login else SURFACE2,
            fg="#161622" if not is_login else TEXT,
            activebackground=GOLD if not is_login else SURFACE2,
        )

        self.submit_btn.configure(
            text="Sign in" if is_login else "Create account"
        )

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