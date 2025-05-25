import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import sqlite3

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

# Dark theme colors - using a darker background
BACKGROUND_COLOR = "#1e1e1e"
FOREGROUND_COLOR = "#ffffff"
BUTTON_BACKGROUND = "#333333"
ENTRY_BACKGROUND = "#2e2e2e"
ACCENT_COLOR = "#4a6984"
SELECTED_COLOR = "#5a7994"
HOVER_COLOR = "#3a5066"

# Email configuration
SENDER_EMAIL = "sgp.noreplydce@gmail.com"
SENDER_PASSWORD = "haub ylen jpof ypse"

class VerificationWindow:
    def __init__(
        self, master, db_manager, auth_manager, username, email, on_verify_success
    ):
        self.master = master
        self.db_manager = db_manager
        self.auth_manager = auth_manager
        self.username = username
        self.email = email
        self.on_verify_success = on_verify_success

        self.master.title("Verify Account")
        self.master.geometry("400x300")
        self.master.resizable(True, True)
        self.master.configure(background=BACKGROUND_COLOR)
        
        # Set icon
        try:
            self.master.iconbitmap(APP_ICON_PATH)
        except tk.TclError:
            pass
        
        # Create and apply custom styles
        self.create_custom_styles()
            
        self.frame = ttk.Frame(self.master, padding="20", style="Dark.TFrame")
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.status_var = tk.StringVar()
        self.status_var.set("Sending verification code...")

        ttk.Label(
            self.frame, 
            text="Email Verification", 
            font=("Arial", 16, "bold"),
            style="Dark.TLabel"
        ).pack(pady=(0, 20))

        email_label = ttk.Label(
            self.frame, 
            text=f"A verification code has been sent to:",
            wraplength=350,
            style="Dark.TLabel"
        )
        email_label.pack(pady=(0, 5))
        
        email_value_label = ttk.Label(
            self.frame, 
            text=email,
            font=("Arial", 10, "italic"),
            wraplength=350,
            style="Dark.TLabel"
        )
        email_value_label.pack(pady=(0, 20))

        code_frame = ttk.Frame(self.frame, style="Dark.TFrame")
        code_frame.pack(fill=tk.X, pady=10)

        ttk.Label(code_frame, text="Enter Code:", style="Dark.TLabel").pack(side=tk.LEFT, padx=5)
        
        self.code_entry = ttk.Entry(
            code_frame, 
            width=10, 
            font=("Arial", 14),
            style="Code.TEntry"
        )
        self.code_entry.pack(side=tk.LEFT, padx=5)
        
        button_frame = ttk.Frame(self.frame, style="Dark.TFrame")
        button_frame.pack(fill=tk.X, pady=20)

        ttk.Button(
            button_frame, 
            text="Verify", 
            command=self.verify,
            style="Dark.TButton"
        ).pack(side=tk.RIGHT, padx=5)

        ttk.Button(
            button_frame, 
            text="Resend Code", 
            command=self.resend_code,
            style="Dark.TButton"
        ).pack(side=tk.RIGHT, padx=5)

        self.status_label = ttk.Label(
            self.frame, 
            textvariable=self.status_var, 
            foreground="#00ff00", 
            font=("Arial", 10),
            style="Status.TLabel"
        )
        self.status_label.pack(pady=10)

        self.master.after(500, self.send_verification)

    def create_custom_styles(self):
        """Create dark theme custom styles for widgets"""
        style = ttk.Style()
        
        # Frame styles
        style.configure("Dark.TFrame", background=BACKGROUND_COLOR)
        
        # Label styles
        style.configure("Dark.TLabel", 
            background=BACKGROUND_COLOR, 
            foreground=FOREGROUND_COLOR)
        
        # Status label style - keeps green text
        style.configure("Status.TLabel",
            background=BACKGROUND_COLOR,
            foreground="#00ff00")
        
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
            
        # Custom entry for verification code
        style.configure("Code.TEntry", 
            foreground=FOREGROUND_COLOR, 
            fieldbackground=ENTRY_BACKGROUND,
            insertcolor=FOREGROUND_COLOR,
            padding=5,
            borderwidth=2)

    def send_verification(self):
        verification_code = self.auth_manager.generate_verification_code()
        print(
            f"Generated verification code: {verification_code} for user {self.username}"
        )

        self.db_manager.execute_query(
            """
            UPDATE users SET verification_code = ? WHERE username = ?
            """,
            (verification_code, self.username),
        )

        success = self.auth_manager.send_verification_email(
            self.email, verification_code, SENDER_EMAIL, SENDER_PASSWORD
        )

        if success:
            self.status_var.set("Verification code sent! Please check your email.")
        else:
            self.status_var.set("Failed to send code. Click Resend to try again.")

    def resend_code(self):
        self.status_var.set("Sending new verification code...")
        self.master.update_idletasks()
        self.send_verification()

    def verify(self):
        code = self.code_entry.get().strip()
        if not code:
            messagebox.showerror("Error", "Please enter the verification code")
            return

        print(f"Checking verification code: {code} for user {self.username}")

        user = self.db_manager.execute_query(
            """
            SELECT id, verification_code, special_sentence FROM users WHERE username = ?
            """,
            (self.username,),
        ).fetchone()

        if user and user[1] == code:
            print(f"Verification successful for user {self.username}")
            self.db_manager.execute_query(
                """
                UPDATE users SET verified = 1 WHERE id = ?
                """,
                (user[0],),
            )

            special_sentence = user[2]
            self.display_special_sentence(special_sentence)

            messagebox.showinfo("Success", "Account verified successfully!")
            self.master.destroy()
            self.on_verify_success()
        else:
            stored_code = user[1] if user and user[1] else "No code found"
            print(f"Verification failed. Entered: {code}, Stored: {stored_code}")
            messagebox.showerror("Error", "Invalid verification code")
            self.status_var.set("Invalid code. Please try again.")

    def display_special_sentence(self, special_sentence):
        try:
            sentence_window = tk.Toplevel(self.master)
            sentence_window.title("Your Special Sentence")
            sentence_window.geometry("500x300")
            sentence_window.resizable(True, True)
            sentence_window.configure(background=BACKGROUND_COLOR)
            
            # Set icon
            try:
                sentence_window.iconbitmap(APP_ICON_PATH)
            except tk.TclError:
                pass
                
            # Configure styles
            style = ttk.Style()
            
            # Configure styles with better contrast
            style.configure("Special.TFrame",
                background=BACKGROUND_COLOR,
                padding=20
            )
            
            style.configure("Special.TLabel",
                font=("Arial", 14, "bold"),
                foreground=FOREGROUND_COLOR,
                background=BACKGROUND_COLOR
            )
            
            style.configure("SpecialText.TLabel",
                font=("Arial", 12),
                foreground=FOREGROUND_COLOR,
                background=BACKGROUND_COLOR,
                wraplength=400,
                justify="center"
            )
            
            style.configure("Special.TButton",
                font=("Arial", 11, "bold"),
                padding=10,
                background=ACCENT_COLOR,
                foreground=FOREGROUND_COLOR
            )
            
            style.map("Special.TButton",
                background=[("active", SELECTED_COLOR), ("pressed", HOVER_COLOR)],
                foreground=[("active", FOREGROUND_COLOR), ("pressed", FOREGROUND_COLOR)]
            )

            frame = ttk.Frame(sentence_window, style="Special.TFrame")
            frame.pack(fill=tk.BOTH, expand=True)

            header_label = ttk.Label(
                frame,
                text="IMPORTANT: Save Your Special Sentence",
                style="Special.TLabel"
            )
            header_label.pack(pady=(0, 20))

            instructions_label = ttk.Label(
                frame,
                text="This sentence can be used to reset your password if you forget it.\nPlease save it in a secure location.",
                style="SpecialText.TLabel"
            )
            instructions_label.pack(pady=(0, 20))

            # Use a Text widget with selection highlighting
            sentence_text = tk.Text(
                frame,
                height=3,
                width=40,
                font=("Arial", 12),
                wrap=tk.WORD,
                background=ENTRY_BACKGROUND,
                foreground=FOREGROUND_COLOR,
                selectbackground=ACCENT_COLOR,  # Selection highlight color
                highlightthickness=1,
                insertbackground=FOREGROUND_COLOR,
                highlightbackground=ACCENT_COLOR
            )
            sentence_text.insert("1.0", special_sentence)
            sentence_text.configure(state="normal")  # Allow copying but not editing
            sentence_text.pack(pady=(0, 20), padx=20, fill=tk.X)

            confirm_button = ttk.Button(
                frame,
                text="I've Saved My Sentence",
                command=sentence_window.destroy,
                style="Special.TButton"
            )
            confirm_button.pack(pady=20)

            # Center the window
            sentence_window.update_idletasks()
            width = sentence_window.winfo_width()
            height = sentence_window.winfo_height()
            x = (sentence_window.winfo_screenwidth() // 2) - (width // 2)
            y = (sentence_window.winfo_screenheight() // 2) - (height // 2)
            sentence_window.geometry(f'+{x}+{y}')

            # Configure window to resize contents
            sentence_window.columnconfigure(0, weight=1)
            sentence_window.rowconfigure(0, weight=1)
            frame.columnconfigure(0, weight=1)
            frame.rowconfigure(3, weight=1)  # Give weight to button row

            sentence_window.transient(self.master)
            sentence_window.grab_set()
            
            self.master.wait_window(sentence_window)
            
        except Exception as e:
            print(f"Error in display_special_sentence: {e}")
            messagebox.showerror(
                "Error",
                "Failed to display special sentence window. Please try again."
            )