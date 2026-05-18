import tkinter as tk
from tkinter import messagebox
from db import login_user, sign_up_user

class LoginScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e2e")
        self.controller = controller

        # Title
        title_label = tk.Label(self, text="🐍 SnakeVault Login", font=("Arial", 24, "bold"), fg="#cdd6f4", bg="#1e1e2e")
        title_label.pack(pady=40)

        # Email Input
        tk.Label(self, text="Email Address", font=("Arial", 12), fg="#a6adc8", bg="#1e1e2e").pack(pady=5)
        self.email_entry = tk.Entry(self, font=("Arial", 12), width=30, bg="#313244", fg="#cdd6f4", insertbackground="white", bd=0, highlightthickness=1)
        self.email_entry.pack(pady=5)

        # Password Input
        tk.Label(self, text="Master Password", font=("Arial", 12), fg="#a6adc8", bg="#1e1e2e").pack(pady=5)
        self.password_entry = tk.Entry(self, font=("Arial", 12), width=30, show="*", bg="#313244", fg="#cdd6f4", insertbackground="white", bd=0, highlightthickness=1)
        self.password_entry.pack(pady=5)

        # Buttons Frame
        btn_frame = tk.Frame(self, bg="#1e1e2e")
        btn_frame.pack(pady=30)

        login_btn = tk.Button(btn_frame, text="Login", font=("Arial", 12, "bold"), width=12, bg="#a6e3a1", fg="#11111b", activebackground="#94e2d5", command=self.handle_login)
        login_btn.pack(side="left", padx=10)

        signup_btn = tk.Button(btn_frame, text="Sign Up", font=("Arial", 12, "bold"), width=12, bg="#89b4fa", fg="#11111b", activebackground="#b4befe", command=self.handle_signup)
        signup_btn.pack(side="right", padx=10)

    def handle_login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showwarning("Error", "Please fill in all fields.")
            return

        result = login_user(email, password)
        if result["success"]:
            self.controller.show_screen("dashboard")
        else:
            messagebox.showerror("Login Failed", result.get("error", "Invalid credentials"))

    def handle_signup(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if not email or not password:
            messagebox.showwarning("Error", "Please fill in all fields.")
            return

        result = sign_up_user(email, password)
        if result["success"]:
            messagebox.showinfo("Success", "Account created successfully! You can now log in.")
        else:
            messagebox.showerror("Sign Up Failed", result.get("error", "Could not register user."))