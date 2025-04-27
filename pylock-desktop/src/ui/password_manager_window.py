import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os
import base64
import secrets
import string
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
APP_ICON_PATH = os.path.join(ICONS_DIR, 'pylock_icon.ico')
ICON_PATH = os.path.join(ICONS_DIR, 'pylock_icon.png')

# Dark theme colors - using a darker background
BACKGROUND_COLOR = "#1e1e1e" # Darker background
FOREGROUND_COLOR = "#ffffff"
BUTTON_BACKGROUND = "#333333"
ENTRY_BACKGROUND = "#2e2e2e"
ACCENT_COLOR = "#4a6984"
SELECTED_COLOR = "#5a7994"
HOVER_COLOR = "#3a5066"

class MainWindow:
    def __init__(self, master, db_manager, encryption_manager, user):
        self.master = master
        self.db_manager = db_manager
        self.encryption_manager = encryption_manager
        self.user = user
        self.selected_service = None
        self.selected_username = None
        self.edited_password_id = None

        self.master.title("PyLock Password Manager")
        
        # Set app icon
        try:
            self.master.iconbitmap(APP_ICON_PATH)
        except tk.TclError:
            # Fallback if .ico file fails
            pass
            
        # Configure rows and columns to be resizable
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        
        # Make the entire window use the dark background
        self.master.configure(background=BACKGROUND_COLOR)
        
        self.frame = ttk.Frame(self.master, padding="10", style="Dark.TFrame")
        self.frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Make frame expandable
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)
        self.frame.rowconfigure(0, weight=1)
        
        # Create and apply custom styles
        self.create_custom_styles()
        
        self.notebook = ttk.Notebook(self.frame, style="Dark.TNotebook")
        self.notebook.grid(row=0, column=0, columnspan=2, pady=10, sticky="nsew")

        self.add_password_tab = ttk.Frame(self.notebook, style="Dark.TFrame")
        self.retrieve_password_tab = ttk.Frame(self.notebook, style="Dark.TFrame")

        self.notebook.add(self.add_password_tab, text="Add Password")
        self.notebook.add(self.retrieve_password_tab, text="Retrieve Password")

        self.setup_add_password_tab()
        self.setup_retrieve_password_tab()

        ttk.Button(self.frame, text="Logout", command=self.logout, style="Dark.TButton").grid(
            column=1, row=1, sticky=tk.E, pady=10
        )
        self.start_auto_logout_timer()
    
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
        
        # Notebook styles
        style.configure("Dark.TNotebook", 
            background=BACKGROUND_COLOR, 
            foreground=FOREGROUND_COLOR,
            borderwidth=0)
        style.configure("Dark.TNotebook.Tab", 
            background=BUTTON_BACKGROUND, 
            foreground=FOREGROUND_COLOR,
            padding=[10, 5],
            focuscolor=ACCENT_COLOR)
        style.map("Dark.TNotebook.Tab",
            background=[("selected", ACCENT_COLOR), ("active", HOVER_COLOR)],
            foreground=[("selected", FOREGROUND_COLOR)])
        
        # Treeview styles
        style.configure("Dark.Treeview",
            background=ENTRY_BACKGROUND,
            foreground=FOREGROUND_COLOR,
            fieldbackground=ENTRY_BACKGROUND)
        style.map("Dark.Treeview",
            background=[("selected", ACCENT_COLOR)])
        
    def setup_add_password_tab(self):
        # Configure tab for expansion
        self.add_password_tab.columnconfigure(1, weight=1)
        for i in range(6):  # Increased for edit mode message
            self.add_password_tab.rowconfigure(i, weight=1)
            
        # Edit mode indicator
        self.edit_mode_var = tk.StringVar()
        self.edit_mode_var.set("")
        self.edit_mode_label = ttk.Label(
            self.add_password_tab, 
            textvariable=self.edit_mode_var, 
            style="Dark.TLabel",
            foreground="#ffaa00",  # Amber color for caution/edit mode
            font=("Arial", 10, "bold")
        )
        self.edit_mode_label.grid(column=0, row=0, columnspan=2, sticky=tk.W, pady=(0, 10))
            
        ttk.Label(self.add_password_tab, text="Service:", style="Dark.TLabel").grid(
            column=0, row=1, sticky=tk.W, pady=5
        )
        self.service_entry = ttk.Entry(self.add_password_tab, width=30, style="Dark.TEntry")
        self.service_entry.grid(column=1, row=1, sticky=(tk.W, tk.E), pady=5, padx=5)

        ttk.Label(self.add_password_tab, text="Username:", style="Dark.TLabel").grid(
            column=0, row=2, sticky=tk.W, pady=5
        )
        self.username_entry = ttk.Entry(self.add_password_tab, width=30, style="Dark.TEntry")
        self.username_entry.grid(column=1, row=2, sticky=(tk.W, tk.E), pady=5, padx=5)

        ttk.Label(self.add_password_tab, text="Password:", style="Dark.TLabel").grid(
            column=0, row=3, sticky=tk.W, pady=5
        )
        self.password_entry = ttk.Entry(self.add_password_tab, show="*", width=30, style="Dark.TEntry")
        self.password_entry.grid(column=1, row=3, sticky=(tk.W, tk.E), pady=5, padx=5)

        button_frame = ttk.Frame(self.add_password_tab, style="Dark.TFrame")
        button_frame.grid(column=0, row=4, columnspan=2, sticky=(tk.E), pady=5)

        ttk.Button(
            button_frame,
            text="Generate Password",
            command=self.generate_password,
            style="Dark.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        self.save_button = ttk.Button(
            button_frame,
            text="Save",
            command=self.save_password,
            style="Dark.TButton"
        )
        self.save_button.pack(side=tk.LEFT, padx=5)
        
        self.cancel_button = ttk.Button(
            button_frame,
            text="Cancel Edit",
            command=self.cancel_edit,
            style="Dark.TButton"
        )
        # Don't pack it initially - only show when editing
        
        # Add hint text
        hint_label = ttk.Label(
            self.add_password_tab,
            text="Add a new password for a website, app, or service.",
            font=("Arial", 9, "italic"),
            foreground="#888888",
            style="Dark.TLabel"
        )
        hint_label.grid(column=0, row=5, columnspan=2, sticky=tk.W, pady=(20, 5), padx=5)

    def setup_retrieve_password_tab(self):
        # Configure the tab to expand
        self.retrieve_password_tab.columnconfigure(0, weight=1)
        self.retrieve_password_tab.columnconfigure(1, weight=1)
        self.retrieve_password_tab.rowconfigure(0, weight=3) # Give treeview more space
        self.retrieve_password_tab.rowconfigure(1, weight=1)
        self.retrieve_password_tab.rowconfigure(2, weight=1)
        
        # Create a treeview with service and username columns
        self.tree = ttk.Treeview(
            self.retrieve_password_tab, 
            columns=("Service", "Username"), 
            show="headings",
            style="Dark.Treeview"
        )
        self.tree.heading("Service", text="Service")
        self.tree.heading("Username", text="Username")
        self.tree.column("Service", width=150)
        self.tree.column("Username", width=150)
        
        self.tree.bind("<Double-1>", self.retrieve_password)  # Bind double-click event
        self.tree.grid(column=0, row=0, columnspan=2, sticky="nsew", pady=5, padx=5)
        
        # Add scrollbar to treeview
        scrollbar = ttk.Scrollbar(self.retrieve_password_tab, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=2, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # Add buttons row
        button_frame = ttk.Frame(self.retrieve_password_tab, style="Dark.TFrame")
        button_frame.grid(column=0, row=1, columnspan=2, sticky="ew", pady=5)
        
        ttk.Button(
            button_frame,
            text="View Password",
            command=lambda: self.retrieve_password(None),
            style="Dark.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Edit Password",
            command=self.edit_password,
            style="Dark.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            button_frame,
            text="Delete Password",
            command=self.delete_password,
            style="Dark.TButton"
        ).pack(side=tk.LEFT, padx=5)
        
        # Results display in a scrollable text widget instead of a label
        result_frame = ttk.Frame(self.retrieve_password_tab, style="Dark.TFrame")
        result_frame.grid(column=0, row=2, columnspan=2, sticky="nsew", pady=10, padx=5)
        result_frame.columnconfigure(0, weight=1)
        result_frame.rowconfigure(0, weight=1)
        
        self.retrieve_result = tk.Text(
            result_frame, 
            font=("Arial", 12), 
            wrap=tk.WORD, 
            height=4,
            background=ENTRY_BACKGROUND,
            foreground=FOREGROUND_COLOR,
            insertbackground=FOREGROUND_COLOR,
            selectbackground=ACCENT_COLOR,
            highlightbackground=BACKGROUND_COLOR,
            highlightcolor=ACCENT_COLOR,
            relief=tk.SUNKEN,
            borderwidth=1
        )
        self.retrieve_result.grid(row=0, column=0, sticky="nsew")
        
        result_scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=self.retrieve_result.yview)
        result_scrollbar.grid(row=0, column=1, sticky="ns")
        self.retrieve_result.configure(yscrollcommand=result_scrollbar.set)
        
        # Populate the treeview with stored services
        self.populate_password_list()
        
    def edit_password(self):
        """Edit the selected password"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an account to edit")
            return
            
        # Get the selected service and username
        service, username = self.tree.item(selected_item, "values")
        
        # Check if the user is authorized to edit this password
        verify_window = self.create_verification_window("Edit Password")
        
        def verify_and_edit():
            entered_sentence = verify_window.sentence_entry.get("1.0", "end-1c").strip()
            
            stored_sentence = self.db_manager.execute_query(
                "SELECT special_sentence FROM users WHERE id = ?",
                (self.user[0],)
            ).fetchone()[0]

            if entered_sentence == stored_sentence:
                verify_window.destroy()
                
                # Get the password details from the database
                password_data = self.db_manager.execute_query(
                    """
                    SELECT id, password, iv FROM passwords
                    WHERE user_id = ? AND service = ? AND username = ?
                    """,
                    (self.user[0], service, username),
                ).fetchone()
                
                if password_data:
                    # Set the edit mode and store the password ID for later saving
                    self.edited_password_id = password_data[0]
                    self.edit_mode_var.set(f"EDIT MODE: Editing account {username} for {service}")
                    
                    # Fill the form with existing data
                    self.service_entry.delete(0, tk.END)
                    self.service_entry.insert(0, service)
                    
                    self.username_entry.delete(0, tk.END)
                    self.username_entry.insert(0, username)
                    
                    # Get the decrypted password
                    decrypted_password = self.encryption_manager.decrypt_password(
                        password_data[1], password_data[2], 
                        base64.urlsafe_b64decode(self.user[1])
                    )
                    
                    self.password_entry.delete(0, tk.END)
                    self.password_entry.insert(0, decrypted_password)
                    
                    # Show the cancel edit button
                    self.cancel_button.pack(side=tk.LEFT, padx=5)
                    
                    # Switch to the add password tab
                    self.notebook.select(self.add_password_tab)
                else:
                    messagebox.showerror("Error", "Password details not found")
            else:
                messagebox.showerror("Error", "Invalid special sentence")
                
        verify_window.bind_verify_button(verify_and_edit)

    def cancel_edit(self):
        """Cancel edit mode and clear the form"""
        self.edited_password_id = None
        self.edit_mode_var.set("")
        
        # Clear the form
        self.service_entry.delete(0, tk.END)
        self.username_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        
        # Hide the cancel button
        self.cancel_button.pack_forget()

    def delete_password(self):
        """Delete a specific password entry"""
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an account to delete")
            return
        
        # Get the selected service and username
        service, username = self.tree.item(selected_item, "values")
        
        confirm = messagebox.askyesno(
            "Confirm Deletion",
            f"Are you sure you want to delete the account '{username}' for '{service}'?"
        )
        
        if confirm:
            verify_window = self.create_verification_window("Delete Password")
            
            def verify_and_delete():
                entered_sentence = verify_window.sentence_entry.get("1.0", "end-1c").strip()
                
                stored_sentence = self.db_manager.execute_query(
                    "SELECT special_sentence FROM users WHERE id = ?",
                    (self.user[0],)
                ).fetchone()[0]

                if entered_sentence == stored_sentence:
                    verify_window.destroy()
                    
                    # Delete the specific password entry
                    self.db_manager.execute_query(
                        """
                        DELETE FROM passwords
                        WHERE user_id = ? AND service = ? AND username = ?
                        """,
                        (self.user[0], service, username),
                    )
                    
                    # Clear the text widget properly
                    self.retrieve_result.delete("1.0", tk.END)
                    
                    # Refresh the password list
                    self.populate_password_list()
                    
                    messagebox.showinfo("Success", f"Account '{username}' for '{service}' has been deleted")
                else:
                    messagebox.showerror("Error", "Invalid special sentence")
                    
            verify_window.bind_verify_button(verify_and_delete)
    
    def create_verification_window(self, action_name):
        """Create a verification window for secure operations"""
        class VerificationWindow:
            def __init__(self, parent, action_name):
                self.window = tk.Toplevel(parent)
                self.window.title(f"Verify Special Sentence - {action_name}")
                self.window.geometry("400x200")
                self.window.resizable(True, True)
                self.window.configure(background=BACKGROUND_COLOR)
                
                # Set app icon
                try:
                    self.window.iconbitmap(APP_ICON_PATH)
                except tk.TclError:
                    pass

                self.frame = ttk.Frame(self.window, padding="20", style="Dark.TFrame")
                self.frame.pack(fill=tk.BOTH, expand=True)

                ttk.Label(
                    self.frame,
                    text=f"Please enter your special sentence to {action_name.lower()}:",
                    wraplength=350,
                    style="Dark.TLabel"
                ).pack(pady=(0, 10))

                # Use a Text widget with selection highlighting
                self.sentence_entry = tk.Text(
                    self.frame,
                    width=30,
                    height=2,
                    font=("Arial", 12),
                    wrap=tk.WORD,
                    background=ENTRY_BACKGROUND,
                    foreground=FOREGROUND_COLOR,
                    selectbackground=ACCENT_COLOR,
                    insertbackground=FOREGROUND_COLOR,
                    highlightthickness=1,
                    highlightbackground=ACCENT_COLOR
                )
                self.sentence_entry.pack(pady=10, fill=tk.X)
                
                self.verify_button = ttk.Button(
                    self.frame,
                    text="Verify",
                    style="Dark.TButton"
                )
                self.verify_button.pack(pady=20)
                
                # Center the window and make it modal
                self.window.transient(parent)
                self.window.grab_set()
                self.window.focus_set()
                
                self.window.update_idletasks()
                width = self.window.winfo_width()
                height = self.window.winfo_height()
                x = (self.window.winfo_screenwidth() // 2) - (width // 2)
                y = (self.window.winfo_screenheight() // 2) - (height // 2)
                self.window.geometry(f'+{x}+{y}')
            
            def bind_verify_button(self, command):
                self.verify_button.config(command=command)
                
            def destroy(self):
                self.window.destroy()
        
        return VerificationWindow(self.master, action_name)

    def generate_password(self):
        chars = string.ascii_letters + string.digits + "!@#$%^&*()"
        password = "".join(secrets.choice(chars) for _ in range(16))
        self.password_entry.delete(0, tk.END)
        self.password_entry.insert(0, password)

    def save_password(self):
        service = self.service_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        if not all([service, username, password]):
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            # Check if we're in edit mode
            if self.edited_password_id is not None:
                # Update the existing password
                encrypted_password, iv = self.encryption_manager.encrypt_password(
                    password, base64.urlsafe_b64decode(self.user[1])
                )
                
                self.db_manager.execute_query(
                    """
                    UPDATE passwords 
                    SET service = ?, username = ?, password = ?, iv = ?
                    WHERE id = ?
                    """,
                    (service, username, encrypted_password, iv, self.edited_password_id),
                )
                
                success_msg = f"Password updated successfully for {username} at {service}"
                
                # Reset edit mode
                self.cancel_edit()
                
            else:
                # Check if username for this service already exists
                existing = self.db_manager.execute_query(
                    """
                    SELECT id FROM passwords 
                    WHERE user_id = ? AND service = ? AND username = ?
                    """,
                    (self.user[0], service, username)
                ).fetchone()
                
                if existing:
                    messagebox.showerror(
                        "Error", 
                        f"Username '{username}' already exists for service '{service}'. Please use a different username."
                    )
                    return

                # Encrypt the password
                encrypted_password, iv = self.encryption_manager.encrypt_password(
                    password, base64.urlsafe_b64decode(self.user[1])
                )

                # Save to database
                self.db_manager.execute_query(
                    """
                    INSERT INTO passwords (user_id, service, username, password, iv)
                    VALUES (?, ?, ?, ?, ?)
                    """,
                    (self.user[0], service, username, encrypted_password, iv),
                )
                
                success_msg = "Password saved successfully"
                
                # Clear input fields
                self.service_entry.delete(0, tk.END)
                self.username_entry.delete(0, tk.END)
                self.password_entry.delete(0, tk.END)
            
            # Update the password list immediately
            self.populate_password_list()
            
            # Switch to the retrieve tab to show the updated list
            self.notebook.select(self.retrieve_password_tab)
            
            messagebox.showinfo("Success", success_msg)
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save password: {str(e)}")

    def retrieve_password(self, event=None):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "Please select an account")
            return
        
        # Get service and username from selection
        service, username = self.tree.item(selected_item, "values")

        verify_window = self.create_verification_window("View Password")

        def verify_and_show():
            entered_sentence = verify_window.sentence_entry.get("1.0", "end-1c").strip()
            
            stored_sentence = self.db_manager.execute_query(
                "SELECT special_sentence FROM users WHERE id = ?",
                (self.user[0],)
            ).fetchone()[0]

            if entered_sentence == stored_sentence:
                verify_window.destroy()
                
                # Fetch the specific password for the selected service and username
                result = self.db_manager.execute_query(
                    """
                    SELECT password, iv FROM passwords
                    WHERE user_id = ? AND service = ? AND username = ?
                    """,
                    (self.user[0], service, username),
                ).fetchone()

                if result:
                    encrypted_password, iv = result
                    
                    # Decrypt the password
                    decrypted_password = self.encryption_manager.decrypt_password(
                        encrypted_password, 
                        iv, 
                        base64.urlsafe_b64decode(self.user[1])
                    )
                    
                    # Display the password
                    self.retrieve_result.delete("1.0", tk.END)
                    self.retrieve_result.insert(tk.END, 
                        f"Service: {service}\n"
                        f"Username: {username}\n"
                        f"Password: {decrypted_password}"
                    )
                else:
                    messagebox.showerror("Error", "Password not found")
            else:
                messagebox.showerror("Error", "Invalid special sentence")

        verify_window.bind_verify_button(verify_and_show)

    def logout(self):
        if hasattr(self, "auto_logout_timer"):
            self.master.after_cancel(self.auto_logout_timer)
        self.master.destroy()
        
    def start_auto_logout_timer(self):
        # Auto logout after 5 minutes of inactivity
        self.auto_logout_timer = self.master.after(300000, self.auto_logout)
        
        # Reset timer when there's user activity
        self.master.bind("<Key>", self.reset_timer)
        self.master.bind("<Button>", self.reset_timer)
        self.master.bind("<MouseWheel>", self.reset_timer)
        
    def reset_timer(self, event=None):
        if hasattr(self, "auto_logout_timer"):
            self.master.after_cancel(self.auto_logout_timer)
        self.auto_logout_timer = self.master.after(300000, self.auto_logout)
        
    def auto_logout(self):
        messagebox.showinfo("Session Expired", "Your session has expired. Logging out.")
        self.logout()

    def populate_password_list(self):
        # Clear existing entries
        self.tree.delete(*self.tree.get_children())
        
        try:
            # Get all password entries for this user with service and username
            passwords = self.db_manager.execute_query(
                """
                SELECT service, username FROM passwords
                WHERE user_id = ? ORDER BY service, username
                """,
                (self.user[0],)
            ).fetchall()
            
            # Add services to tree
            for service, username in passwords:
                self.tree.insert("", "end", values=(service, username))
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load passwords: {str(e)}")