import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
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

class ResetPasswordWindow:
    def __init__(self, master, db_manager, auth_manager):
        self.master = master
        self.db_manager = db_manager
        self.auth_manager = auth_manager

        self.master.title("Reset Password")
        self.frame = ttk.Frame(self.master, padding="10")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.master.resizable(True, True)
        
        # Set icon
        try:
            self.master.iconbitmap(APP_ICON_PATH)
        except tk.TclError:
            pass

        ttk.Label(self.frame, text="Username:").grid(
            column=0, row=0, sticky=tk.W, pady=5
        )
        self.username_entry = ttk.Entry(self.frame, width=30)
        self.username_entry.grid(column=1, row=0, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(self.frame, text="Special Sentence:").grid(
            column=0, row=1, sticky=tk.W, pady=5
        )
        self.sentence_entry = ttk.Entry(self.frame, width=30)
        self.sentence_entry.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=5)

        ttk.Label(self.frame, text="New Password:").grid(
            column=0, row=2, sticky=tk.W, pady=5
        )
        self.new_password_entry = ttk.Entry(self.frame, show="*", width=30)
        self.new_password_entry.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(
            self.frame,
            text="Generate Password",
            command=self.generate_password
        ).grid(column=1, row=3, sticky=tk.E, pady=5)

        ttk.Button(self.frame, text="Reset Password", command=self.reset_password).grid(
            column=1, row=4, sticky=tk.E, pady=10
        )

    def generate_password(self):
        """Generate a secure random password"""
        chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        password = "".join(secrets.choice(chars) for _ in range(16))
        self.new_password_entry.delete(0, tk.END)
        self.new_password_entry.insert(0, password)
        
    def reset_password(self):
        username = self.username_entry.get()
        special_sentence = self.sentence_entry.get()
        new_password = self.new_password_entry.get()
        
        if not all([username, special_sentence, new_password]):
            messagebox.showerror("Error", "All fields are required")
            return

        user = self.db_manager.execute_query(
            """
            SELECT id, special_sentence FROM users WHERE username = ?
            """,
            (username,),
        ).fetchone()

        if not user:
            messagebox.showerror("Error", "Username not found")
            return
            
        if user[1] != special_sentence:
            messagebox.showerror("Error", "Invalid special sentence")
            return

        # Special sentence matches, reset password
        derived_key, salt = self.auth_manager.hash_password(new_password)
        self.db_manager.execute_query(
            """
            UPDATE users SET password_hash = ?, salt = ? WHERE id = ?
            """,
            (derived_key, salt, user[0]),
        )
        messagebox.showinfo("Success", "Password reset successfully!")
        self.master.destroy()