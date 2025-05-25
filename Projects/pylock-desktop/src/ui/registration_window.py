import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import sqlite3
import secrets
import string

# Get the base directory for resources
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle/executable
    base_dir = sys._MEIPASS
else:
    # If the application is run as a script
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Define paths for icons
ASSETS_DIR = os.path.join(base_dir, 'assets')
ICONS_DIR = os.path.join(ASSETS_DIR, 'icons')

# Icon path
APP_ICON_PATH = os.path.join(ICONS_DIR, 'pylock_icon.ico')

# Import internal module for verification after we define the icon path
from ui.verification_window import VerificationWindow

class RegistrationWindow:
    def __init__(self, master, db_manager, auth_manager):
        self.master = master
        self.db_manager = db_manager
        self.auth_manager = auth_manager

        self.master.title("Register")
        self.frame = ttk.Frame(self.master, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.master.resizable(True, True)
        
        # Set window icon
        try:
            self.master.iconbitmap(APP_ICON_PATH)
        except tk.TclError:
            pass

        ttk.Label(self.frame, text="Username:").grid(
            column=0, row=0, sticky=tk.W, pady=5
        )
        self.username_entry = ttk.Entry(self.frame, width=30)
        self.username_entry.grid(column=1, row=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(self.frame, text="Password:").grid(
            column=0, row=1, sticky=tk.W, pady=5
        )
        self.password_entry = ttk.Entry(self.frame, show="*", width=30)
        self.password_entry.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(
            self.frame,
            text="Generate Password",
            command=self.generate_password
        ).grid(column=1, row=2, sticky=tk.E, pady=5)

        ttk.Label(self.frame, text="Email:").grid(column=0, row=3, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(self.frame, width=30)
        self.email_entry.grid(column=1, row=3, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(self.frame, text="Phone:").grid(column=0, row=4, sticky=tk.W, pady=5)
        self.phone_entry = ttk.Entry(self.frame, width=30)
        self.phone_entry.grid(column=1, row=4, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(self.frame, text="Register", command=self.register).grid(
            column=1, row=5, sticky=tk.E, pady=10
        )
    
    def generate_password(self):
        chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        password = "".join(secrets.choice(chars) for _ in range(16))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        email = self.email_entry.get()
        phone = self.phone_entry.get()

        if not all([username, password, email, phone]):
            messagebox.showerror("Error", "All fields are required")
            return

        derived_key, salt = self.auth_manager.hash_password(password)
        verification_code = self.auth_manager.generate_verification_code()
        special_sentence = self.auth_manager.generate_special_sentence()

        try:
            self.db_manager.execute_query(
                """
                INSERT INTO users (username, password_hash, salt, email, phone, verified, special_sentence)
                VALUES (?, ?, ?, ?, ?, 0, ?)
                """,
                (username, derived_key, salt, email, phone, special_sentence),
            )

            verification_code = self.auth_manager.generate_verification_code()
            self.db_manager.execute_query(
                """
                UPDATE users SET verification_code = ? WHERE username = ?
                """,
                (verification_code, username),
            )

            self.master.destroy()

            verification_window = tk.Toplevel(self.master.master)
            verification_window.title("Verify Email")
            try:
                verification_window.iconbitmap(APP_ICON_PATH)
            except tk.TclError:
                pass
                
            VerificationWindow(
                verification_window,
                self.db_manager,
                self.auth_manager,
                username,
                email,
                lambda: messagebox.showinfo(
                    "Success", "You can now log in with your credentials."
                ),
            )

        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")