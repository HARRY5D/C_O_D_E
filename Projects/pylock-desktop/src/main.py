import tkinter as tk
import sys
import os
from tkinter import ttk, messagebox
from PIL import Image, ImageTk

# Get the base directory for resources
if getattr(sys, 'frozen', False):
    # If the application is run as a bundle/executable
    base_dir = sys._MEIPASS
else:
    # If the application is run as a script
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Define paths
ASSETS_DIR = os.path.join(base_dir, 'assets')
ICONS_DIR = os.path.join(ASSETS_DIR, 'icons')

# Icon paths
LOGO_PATH = os.path.join(ICONS_DIR, 'pylock_logo.png')
APP_ICON_PATH = os.path.join(ICONS_DIR, 'pylock_icon.ico')
ICON_PATH = os.path.join(ICONS_DIR, 'pylock_icon.png')

# Get user's app data directory for database
APP_DATA_DIR = os.path.join(os.path.expanduser('~'), 'PyLock')
os.makedirs(APP_DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(APP_DATA_DIR, 'passwords.db')

# Email configuration
SENDER_EMAIL = "sgp.noreplydce@gmail.com"
SENDER_PASSWORD = "haub ylen jpof ypse"

# Import internal modules
from database.db_manager import DatabaseManager
from encryption.encryption_manager import EncryptionManager, AuthManager
from ui.login_window import LoginWindow
from ui.password_manager_window import MainWindow

class PasswordManagerApp:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.auth_manager = AuthManager()
        self.encryption_manager = EncryptionManager()

        self.root = tk.Tk()
        self.root.title("PyLock Password Manager")
        self.root.geometry("600x500")
        self.root.resizable(True, True)  # Ensure main window is resizable
        
        # Set app icon
        try:
            self.root.iconbitmap(APP_ICON_PATH)
        except tk.TclError:
            # Fallback if .ico file fails
            pass
            
        # Configure dark theme
        self.configure_dark_theme()
        
        # Center window on screen
        self.center_window(self.root, 600, 500)
        
        self.show_login_window()
    
    def center_window(self, window, width, height):
        # Get screen dimensions
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        
        # Calculate position
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        
        # Set window geometry
        window.geometry(f'{width}x{height}+{x}+{y}')
    
    def configure_dark_theme(self):
        style = ttk.Style()
        
        # Try to use clam theme as base
        if "clam" in style.theme_names():
            style.theme_use("clam")
        
        # Dark theme colors
        bg_color = "#2e2e2e"
        fg_color = "#ffffff"
        button_bg = "#3d3d3d"
        entry_bg = "#1e1e1e"
        accent_color = "#4a6984"
        
        # Configure common elements
        style.configure("TFrame", background=bg_color)
        style.configure("TLabel", background=bg_color, foreground=fg_color)
        style.configure("TButton", 
                       background=button_bg, 
                       foreground=fg_color,
                       focuscolor=accent_color,
                       borderwidth=1,
                       padding=5)
        style.map("TButton",
                 background=[("active", accent_color), ("pressed", "#2a3f50")],
                 relief=[("pressed", "sunken")])
        
        style.configure("TEntry",
                       foreground=fg_color,
                       fieldbackground=entry_bg,
                       insertcolor=fg_color,
                       borderwidth=1,
                       padding=5)
                       
        style.configure("TNotebook", background=bg_color, borderwidth=0)
        style.configure("TNotebook.Tab", 
                       background=button_bg, 
                       foreground=fg_color,
                       padding=[10, 5],
                       focuscolor=accent_color)
        style.map("TNotebook.Tab",
                 background=[("selected", accent_color), ("active", "#3a5066")],
                 foreground=[("selected", "#ffffff")])
                 
        style.configure("Treeview",
                       background=entry_bg,
                       foreground=fg_color,
                       fieldbackground=entry_bg)
        style.map("Treeview",
                 background=[("selected", accent_color)])
        
        # Configure the root window background
        self.root.configure(background=bg_color)
        
        # Make all popup windows use the same theme
        self.root.option_add("*TkDefaultFont", "Arial 10")
        self.root.option_add("*Background", bg_color)
        self.root.option_add("*Foreground", fg_color)
        
        # Enable all popups to be resizable
        self.root.option_add("*resizable", True)
    
    def show_login_window(self):
        LoginWindow(
            self.root, self.db_manager, self.auth_manager, self.on_login_success
        )

    def on_login_success(self, user):
        for widget in self.root.winfo_children():
            widget.destroy()
        MainWindow(self.root, self.db_manager, self.encryption_manager, user)
    
    def run(self):
        self.root.mainloop()


def create_desktop_shortcut():
    """Create a desktop shortcut to the application"""
    try:
        import winshell
        from win32com.client import Dispatch
        
        desktop = winshell.desktop()
        path = os.path.join(desktop, "PyLock Password Manager.lnk")
        
        if not os.path.exists(path):
            target = sys.executable if getattr(sys, 'frozen', False) else __file__
            
            shell = Dispatch('WScript.Shell')
            shortcut = shell.CreateShortCut(path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = os.path.dirname(target)
            shortcut.IconLocation = APP_ICON_PATH
            shortcut.save()
            print(f"Desktop shortcut created at {path}")
        
    except ImportError:
        print("Could not create desktop shortcut: winshell or win32com module not found")
    except Exception as e:
        print(f"Error creating desktop shortcut: {e}")


if __name__ == "__main__":
    # Create desktop shortcut if running on Windows
    if os.name == 'nt':
        create_desktop_shortcut()
        
    app = PasswordManagerApp()
    app.run()