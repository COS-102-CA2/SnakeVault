import tkinter as tk
from tkinter import messagebox, ttk
from db import fetch_user_passwords, save_password, logout_user

class DashboardScreen(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1e1e2e")
        self.controller = controller

        # --- Top Navigation Panel ---
        nav_panel = tk.Frame(self, bg="#11111b", height=50)
        nav_panel.pack(fill="x", side="top")

        welcome_lbl = tk.Label(nav_panel, text="🔒 Your Secure Vault", font=("Arial", 14, "bold"), fg="#cdd6f4", bg="#11111b")
        welcome_lbl.pack(side="left", padx=20, pady=10)

        logout_btn = tk.Button(nav_panel, text="Logout", bg="#f38ba8", fg="#11111b", command=self.handle_logout)
        logout_btn.pack(side="right", padx=20, pady=10)

        # --- Main Layout Split ---
        # Left Panel: Adding a new password
        self.left_panel = tk.Frame(self, bg="#181825", width=250)
        self.left_panel.pack(side="left", fill="y", padx=10, pady=10)
        self.setup_add_form()

        # Right Panel: Displaying saved passwords
        right_panel = tk.Frame(self, bg="#1e1e2e")
        right_panel.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        # Treeview to display credentials
        self.tree = ttk.Treeview(right_panel, columns=("Site", "URL", "Username", "Password"), show="headings")
        self.tree.heading("Site", text="Site Name")
        self.tree.heading("URL", text="URL")
        self.tree.heading("Username", text="Username")
        self.tree.heading("Password", text="Password (Encrypted)")
        self.tree.pack(fill="both", expand=True)

        # Refresh button
        refresh_btn = tk.Button(right_panel, text="🔄 Refresh Vault", bg="#89b4fa", command=self.load_vault_data)
        refresh_btn.pack(pady=10)

        # Load data on open
        self.load_vault_data()

    def setup_add_form(self):
        """Creates form elements to add a credential."""
        tk.Label(self.left_panel, text="Add New Credential", font=("Arial", 12, "bold"), fg="#cdd6f4", bg="#181825").pack(pady=10)

        tk.Label(self.left_panel, text="Site Name", fg="#a6adc8", bg="#181825").pack()
        self.site_entry = tk.Entry(self.left_panel, bg="#313244", fg="#cdd6f4", bd=0)
        self.site_entry.pack(pady=5, padx=10, fill="x")

        tk.Label(self.left_panel, text="URL", fg="#a6adc8", bg="#181825").pack()
        self.url_entry = tk.Entry(self.left_panel, bg="#313244", fg="#cdd6f4", bd=0)
        self.url_entry.pack(pady=5, padx=10, fill="x")

        tk.Label(self.left_panel, text="Username/Email", fg="#a6adc8", bg="#181825").pack()
        self.user_entry = tk.Entry(self.left_panel, bg="#313244", fg="#cdd6f4", bd=0)
        self.user_entry.pack(pady=5, padx=10, fill="x")

        tk.Label(self.left_panel, text="Password", fg="#a6adc8", bg="#181825").pack()
        self.pass_entry = tk.Entry(self.left_panel, bg="#313244", fg="#cdd6f4", bd=0)
        self.pass_entry.pack(pady=5, padx=10, fill="x")

        save_btn = tk.Button(self.left_panel, text="Save to Vault", bg="#a6e3a1", fg="#11111b", command=self.handle_save)
        save_btn.pack(pady=20, padx=10, fill="x")

    def handle_save(self):
        site = self.site_entry.get().strip()
        url = self.url_entry.get().strip()
        user = self.user_entry.get().strip()
        password = self.pass_entry.get().strip()

        if not site or not user or not password:
            messagebox.showwarning("Validation Error", "Site, Username, and Password fields are required.")
            return

        # Passing straight to db for now. Next step we encrypt 'password' here first!
        result = save_password(site, url, user, password)
        if result["success"]:
            messagebox.showinfo("Saved", "Credential safely stored!")
            self.load_vault_data()
            # Clear fields
            self.site_entry.delete(0, tk.END)
            self.url_entry.delete(0, tk.END)
            self.user_entry.delete(0, tk.END)
            self.pass_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", result.get("error", "Could not save entry."))

    def load_vault_data(self):
        """Clears treeview and reloads data from Supabase."""
        for row in self.tree.get_children():
            self.tree.delete(row)

        result = fetch_user_passwords()
        if result["success"]:
            for item in result["data"]:
                self.tree.insert("", "end", values=(item["site_name"], item["url"], item["username"], item["encrypted_password"]))
        else:
            messagebox.showerror("Error", "Could not fetch vault items.")

    def handle_logout(self):
        logout_user()
        self.controller.show_screen("login")