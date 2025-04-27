import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import sqlite3
from PIL import Image, ImageTk

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

# Icon paths
LOGO_PATH = os.path.join(ICONS_DIR, 'pylock_logo.png')
APP_ICON_PATH = os.path.join(ICONS_DIR, 'pylock_icon.ico')

# Dark theme colors - using a darker background
BACKGROUND_COLOR = "#1e1e1e" # Darker background
FOREGROUND_COLOR = "#ffffff"
BUTTON_BACKGROUND = "#333333"
ENTRY_BACKGROUND = "#2e2e2e"
ACCENT_COLOR = "#4a6984"
SELECTED_COLOR = "#5a7994"
HOVER_COLOR = "#3a5066"

from ui.registration_window import RegistrationWindow
from ui.verification_window import VerificationWindow
from ui.reset_password_window import ResetPasswordWindow

class LoginWindow:
    def __init__(self, master, db_manager, auth_manager, on_login_success):
        self.master = master
        self.db_manager = db_manager
        self.auth_manager = auth_manager
        self.on_login_success = on_login_success

        # Create and apply custom styles
        self.create_custom_styles()

        # Apply the dark background to the entire window
        self.master.configure(background=BACKGROUND_COLOR)
        
        self.frame = ttk.Frame(self.master, padding="20", style="Dark.TFrame")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.master.resizable(True, True)
        
        # Set window icon
        try:
            self.master.iconbitmap(APP_ICON_PATH)
        except tk.TclError:
            # Fallback if .ico file fails
            pass
            
        # Add PyLock Logo
        try:
            logo_img = Image.open(LOGO_PATH)
            logo_img = logo_img.resize((200, 100), Image.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(
                self.frame, 
                image=self.logo, 
                background=BACKGROUND_COLOR,
                borderwidth=0
            )
            logo_label.grid(column=0, row=0, columnspan=2, pady=20)
        except Exception as e:
            print(f"Error loading logo: {e}")
        
        # Setup login UI
        ttk.Label(self.frame, text="Username:", style="Dark.TLabel").grid(
            column=0, row=1, sticky=tk.W, pady=5
        )
        self.username_entry = ttk.Entry(self.frame, width=30, style="Dark.TEntry")
        self.username_entry.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(self.frame, text="Password:", style="Dark.TLabel").grid(
            column=0, row=2, sticky=tk.W, pady=5
        )
        self.password_entry = ttk.Entry(self.frame, show="*", width=30, style="Dark.TEntry")
        self.password_entry.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(self.frame, text="Login", command=self.login, style="Dark.TButton").grid(
            column=1, row=3, sticky=tk.E, pady=10
        )
        ttk.Button(self.frame, text="Register", command=self.open_registration, style="Dark.TButton").grid(
            column=0, row=3, sticky=tk.W, pady=10
        )
        ttk.Button(
            self.frame, text="Forgot Password", command=self.open_reset_password, style="Dark.TButton"
        ).grid(column=1, row=4, sticky=tk.E, pady=10)

    def create_custom_styles(self):
        """Create dark theme custom styles for widgets"""
        style = ttk.Style()
        
        # Frame styles
        style.configure("Dark.TFrame", background=BACKGROUND_COLOR)
        
        # Label styles
        style.configure("Dark.TLabel", 
            background=BACKGROUND_COLOR, 
            foreground=FOREGROUND_COLOR)
        
        # Button styles
        style.configure("Dark.TButton", 
            background=BUTTON_BACKGROUND, 
            foreground=FOREGROUND_COLOR,
            focuscolor=ACCENT_COLOR,
            borderwidth=1,
            padding=5)
        style.map("Dark.TButton",
            background=[("active", ACCENT_COLOR), ("pressed", HOVER_COLOR)],
            relief=[("pressed", "sunken")])
        
        # Entry styles
        style.configure("Dark.TEntry",
            foreground=FOREGROUND_COLOR,
            fieldbackground=ENTRY_BACKGROUND,
            insertcolor=FOREGROUND_COLOR,
            borderwidth=1,
            padding=5)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        user = self.db_manager.execute_query(
            """
            SELECT id, password_hash, salt, verified, email, special_sentence FROM users 
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

        if user:
            stored_key = user[1]
            salt = bytes.fromhex(user[2])
            derived_key, _ = self.auth_manager.hash_password(password, salt)

            if derived_key == stored_key:
                if user[3] == 0:  # If not verified
                    verification_window = tk.Toplevel(self.master)
                    verification_window.configure(background=BACKGROUND_COLOR)
                    VerificationWindow(
                        verification_window,
                        self.db_manager,
                        self.auth_manager,
                        username,
                        user[4],  # email
                        lambda: self.show_special_sentence(user),
                    )
                    return
                self.show_special_sentence(user)
                return

        messagebox.showerror("Error", "Invalid credentials")

    def show_special_sentence(self, user):
        # Only show the special sentence if it's the first login after registration
        # Use a flag in the database to track this or add a session variable
        
        first_login = self.db_manager.execute_query(
            """
            SELECT first_login FROM users WHERE id = ?
            """,
            (user[0],)
        ).fetchone()
        
        # If first_login flag doesn't exist, add it to the users table
        if first_login is None:
            try:
                self.db_manager.execute_query(
                    """
                    ALTER TABLE users ADD COLUMN first_login INTEGER DEFAULT 1
                    """
                )
                first_login = (1,)  # Default to showing on first login
            except sqlite3.OperationalError:
                # Column already exists but no value
                self.db_manager.execute_query(
                    """
                    UPDATE users SET first_login = 1 WHERE id = ?
                    """,
                    (user[0],)
                )
                first_login = (1,)
        
        if first_login[0] == 1 and user[5]:  # If it's first login and special sentence exists
            sentence_window = tk.Toplevel(self.master)
            sentence_window.title("Your Special Sentence")
            sentence_window.geometry("500x300")
            sentence_window.resizable(True, True)
            sentence_window.configure(background=BACKGROUND_COLOR)

            frame = ttk.Frame(sentence_window, padding="20", style="Dark.TFrame")
            frame.pack(fill=tk.BOTH, expand=True)

            ttk.Label(
                frame,
                text="IMPORTANT: Save Your Special Sentence",
                font=("Arial", 14, "bold"),
                style="Dark.TLabel"
            ).pack(pady=(0, 20))

            ttk.Label(
                frame,
                text="This is your special sentence for password retrieval.\nKeep it safe!",
                wraplength=400,
                justify=tk.CENTER,
                style="Dark.TLabel"
            ).pack(pady=(0, 20))

            # Use a Text widget with selection highlighting instead of Entry
            sentence_text = tk.Text(
                frame, 
                width=40, 
                height=3,
                font=("Arial", 12),
                wrap=tk.WORD,
                selectbackground=ACCENT_COLOR,  # Selection highlight color
                highlightthickness=1,
                highlightbackground=ACCENT_COLOR,
                background=ENTRY_BACKGROUND,
                foreground=FOREGROUND_COLOR,
                insertbackground=FOREGROUND_COLOR
            )
            sentence_text.insert("1.0", user[5])
            sentence_text.configure(state="normal")
            sentence_text.pack(pady=10, fill=tk.X, expand=True)

            def proceed():
                # Update first_login flag to 0 so it won't show again
                self.db_manager.execute_query(
                    """
                    UPDATE users SET first_login = 0 WHERE id = ?
                    """,
                    (user[0],)
                )
                sentence_window.destroy()
                self.on_login_success(user)

            ttk.Button(
                frame,
                text="I've Saved My Sentence",
                command=proceed,
                style="Dark.TButton"
            ).pack(pady=20)

            # Make window modal
            sentence_window.transient(self.master)
            sentence_window.grab_set()
            sentence_window.focus_set()
            
            # Configure window to resize contents with it
            sentence_window.columnconfigure(0, weight=1)
            sentence_window.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)
            for i in range(5):  # For all rows in the frame
                frame.rowconfigure(i, weight=1)
        else:
            # If not first login, proceed directly
            self.on_login_success(user)

    def open_registration(self):
        registration_window = tk.Toplevel(self.master)
        registration_window.title("Register")
        registration_window.configure(background=BACKGROUND_COLOR)
        try:
            registration_window.iconbitmap(APP_ICON_PATH)
        except tk.TclError:
            pass
        RegistrationWindow(registration_window, self.db_manager, self.auth_manager)

    def open_reset_password(self):
        reset_password_window = tk.Toplevel(self.master)
        reset_password_window.title("Reset Password")
        reset_password_window.configure(background=BACKGROUND_COLOR)
        try:
            reset_password_window.iconbitmap(APP_ICON_PATH)
        except tk.TclError:
            pass
        ResetPasswordWindow(reset_password_window, self.db_manager, self.auth_manager)