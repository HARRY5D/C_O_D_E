# import ttkbootstrap as ttk

# def apply_styles(root):
#     style = ttk.Style()
#     style.theme_use('darkly')

#     COLORS = {
#         'primary': '#39FF14',          # Neon green
#         'secondary': '#1F1F1F',        # Dark gray
#         'bg_dark': '#000000',          # Pure black
#         'bg_light': '#0A0A0A',         # Slightly lighter black
#         'text': '#FFFFFF',             # White text
#         'input_bg': '#121212',         # Dark input background
#         'border': '#39FF14',           # Neon green border
#         'error': '#FF0033',            # Bright red
#         'hover': '#32CD32'             # Lighter green for hover
        
#     }

#     COMMON_FONT = ('Segoe UI', 10)
#     HEADER_FONT = ('Segoe UI', 24, 'bold')
    
#     # Window style
#     root.configure(bg=COLORS['bg_dark'])
    
#     # Label styles
#     style.configure('TLabel',
#         font=COMMON_FONT,
#         foreground=COLORS['text'],
#         background=COLORS['bg_dark'])

#     style.configure('Header.TLabel',
#         font=HEADER_FONT,
#         foreground=COLORS['primary'],
#         background=COLORS['bg_dark'])

#     # Entry styles with neon accents
#     style.configure('TEntry',
#         fieldbackground=COLORS['input_bg'],
#         foreground=COLORS['text'],
#         insertcolor=COLORS['primary'],
#         font=COMMON_FONT,
#         padding=10,
#         borderwidth=2,
#         relief='solid')

#     # Button styles with neon effects
#     style.configure('Primary.TButton',
#         font=('Segoe UI', 12, 'bold'),
#         background=COLORS['primary'],
#         foreground=COLORS['bg_dark'],
#         padding=(20, 10),
#         borderwidth=0)

#     style.map('Primary.TButton',
#         background=[('active', COLORS['hover'])],
#         foreground=[('active', COLORS['bg_dark'])])

#     style.configure('Secondary.TButton',
#         font=('Segoe UI', 12, 'bold'),
#         background=COLORS['secondary'],
#         foreground=COLORS['primary'],
#         padding=(20, 10),
#         borderwidth=2,
#         relief='solid')

#     style.map('Secondary.TButton',
#         background=[('active', COLORS['bg_light'])],
#         foreground=[('active', COLORS['primary'])])

#     # Frame with neon borders
#     style.configure('TFrame',
#         background=COLORS['bg_dark'],
#         borderwidth=2,
#         relief='solid',
#         bordercolor=COLORS['border'])

#     # Notebook with modern tabs
#     style.configure('TNotebook',
#         background=COLORS['bg_dark'],
#         borderwidth=0)

#     style.configure('TNotebook.Tab',
#         font=('Segoe UI', 11, 'bold'),
#         padding=(15, 8),
#         background=COLORS['bg_light'],
#         foreground=COLORS['primary'])

#     style.map('TNotebook.Tab',
#         background=[('selected', COLORS['bg_dark'])],
#         foreground=[('selected', COLORS['primary'])])

#     # Custom styles for special elements
#     style.configure('Title.TLabel',
#         font=('Segoe UI', 32, 'bold'),
#         foreground=COLORS['primary'],
#         background=COLORS['bg_dark'])

#     style.configure('Subtitle.TLabel',
#         font=('Segoe UI', 14),
#         foreground=COLORS['text'],
#         background=COLORS['bg_dark'])

#     style.configure('Danger.TButton',
#         font=('Segoe UI', 12, 'bold'),
#         background=COLORS['error'],
#         foreground=COLORS['text'],
#         padding=(20, 10),
#         borderwidth=0)
#  # LabelFrame styles
#     style.configure('TLabelframe',
#         background=COLORS['bg_dark'],
#         foreground=COLORS['primary'],
#         bordercolor=COLORS['border'])

#     style.configure('TLabelframe.Label',
#         font=('Segoe UI', 11, 'bold'),
#         foreground=COLORS['primary'],
#         background=COLORS['bg_dark'])

#     # Treeview styles
#     style.configure('Treeview',
#         background=COLORS['bg_dark'],
#         foreground=COLORS['text'],
#         fieldbackground=COLORS['bg_dark'])

#     style.configure('Treeview.Heading',
#         background=COLORS['secondary'],
#         foreground=COLORS['primary'],
#         font=('Segoe UI', 10, 'bold'))

#     # Danger button
#     style.configure('Danger.TButton',
#         font=('Segoe UI', 12, 'bold'),
#         background=COLORS['error'],
#         foreground=COLORS['text'],
#         padding=(20, 10),
#         borderwidth=0)

#     # Canvas style
#     style.configure('TCanvas',
#         background=COLORS['bg_dark'],
#         borderwidth=0,
#         relief='flat')

#     return style


# import ttkbootstrap as ttk
# from ttkbootstrap.constants import *

# def apply_styles(root):
#     # Define the color palette
#     COLORS = {
#         'primary': '#39FF14',  # Neon green
#         'secondary': '#1F1F1F',  # Dark gray
#         'bg_dark': '#000000',  # Pure black
#         'bg_light': '#0A0A0A',  # Slightly lighter black
#         'text': '#FFFFFF',  # White text
#         'input_bg': '#121212',  # Dark input background
#         'border': '#39FF14',  # Neon green border
#         'error': '#FF0033',  # Bright red
#         'hover': '#32CD32'  # Lighter green for hover
#     }

#     # Set theme to 'darkly' for a modern look
#     style = ttk.Style()
#     style.theme_use('darkly')

#     # Apply background color to main window
#     root.configure(bg=COLORS['bg_dark'])

#     # Fonts
#     COMMON_FONT = ('Segoe UI', 10)
#     HEADER_FONT = ('Segoe UI', 24, 'bold')

#     # Labels
#     style.configure('TLabel',
#         font=COMMON_FONT,
#         foreground=COLORS['primary'],#neon green text
#         background=COLORS['bg_dark'])

#     style.configure('Header.TLabel',
#         font=HEADER_FONT,
#         foreground=COLORS['primary'],
#         background=COLORS['bg_dark'])

#     # Entry Fields
#     style.configure('TEntry',
#         fieldbackground=COLORS['bg_dark'],
#         foreground=COLORS['primary'],#font color
#         insertcolor=COLORS['text'],#cursor
#         font=COMMON_FONT,
#         padding=10,
#         borderwidth=2,
#         relief='solid')

#     # Primary Button (Neon Green)
#     style.configure('Primary.TButton',
#         font=('Segoe UI', 12, 'bold'),
#         background=COLORS['primary'],
#         foreground=COLORS['bg_dark'],
#         padding=(20, 10),
#         borderwidth=0)
#     #hover effect
#     style.map('Primary.TButton',
#         background=[('active', COLORS['hover'])],
#         foreground=[('active', COLORS['bg_dark'])])

#     # Secondary Button (Dark Gray)
#     style.configure('Secondary.TButton',
#         font=('Segoe UI', 12, 'bold'),
#         background=COLORS['bg_dark'],
#         foreground=COLORS['primary'],
#         padding=(20, 10),
#         borderwidth=2,
#         relief='solid')

#     style.map('Secondary.TButton',
#         background=[('active', COLORS['bg_dark'])],
#         foreground=[('active', COLORS['primary'])])

#     # Error Button (Red)
#     style.configure('Danger.TButton',
#         font=('Segoe UI', 12, 'bold'),
#         background=COLORS['error'],
#         foreground=COLORS['text'],
#         padding=(20, 10),
#         borderwidth=0)

#     # Frames with neon border
#     style.configure('TFrame',
#         background=COLORS['border'],
#         borderwidth=3,
#         relief='solid')

#     # Notebook (Tabs)
#     style.configure('TNotebook',
#         background=COLORS['bg_dark'],
#         borderwidth=0)

#     style.configure('TNotebook.Tab',
#         font=('Segoe UI', 11, 'bold'),
#         padding=(15, 8),
#         background=COLORS['bg_dark'],
#         foreground=COLORS['primary'])

#     style.map('TNotebook.Tab',
#         background=[('selected', COLORS['bg_dark'])],
#         foreground=[('selected', COLORS['primary'])])

#     # Labels for sections
#     style.configure('Title.TLabel',
#         font=('Segoe UI', 32, 'bold'),
#         foreground=COLORS['primary'],
#         background=COLORS['bg_dark'])

#     style.configure('Subtitle.TLabel',
#         font=('Segoe UI', 14),
#         foreground=COLORS['primary'],
#         background=COLORS['bg_dark'])

#     # LabelFrame (for grouping)
#     style.configure('TLabelframe',
#         background=COLORS['bg_dark'],
#         foreground=COLORS['primary'],
#         bordercolor=COLORS['border'])

#     style.configure('TLabelframe.Label',
#         font=('Segoe UI', 11, 'bold'),
#         foreground=COLORS['primary'],
#         background=COLORS['bg_dark'])

#     # Treeview (Tables)
#     style.configure('Treeview',
#         background=COLORS['bg_dark'],
#         foreground=COLORS['text'],
#         fieldbackground=COLORS['bg_dark'])

#     style.configure('Treeview.Heading',
#         background=COLORS['secondary'],
#         foreground=COLORS['primary'],
#         font=('Segoe UI', 10, 'bold'))

#     # Canvas (for graphs, charts, etc.)
#     style.configure('TCanvas',
#         background=COLORS['bg_dark'],
#         borderwidth=0,
#         relief='flat')

#     return style


#2nd edit white color and 1st is black 
# import ttkbootstrap as ttk
# from ttkbootstrap.constants import *

# def apply_styles(root):
#     style = ttk.Style()
#     style.theme_use('darkly')

#     COLORS = {
#         'primary': '#39FF14',          # Neon green
#         'secondary': '#1F1F1F',        # Dark gray
#         'bg_dark': '#000000',          # Pure black
#         'text': '#FFFFFF',             # White text
#         'text_dark': '#000000',        # Black text for button text
#         'input_bg': '#121212',         # Dark input background
#         'hover': '#32CD32'             # Lighter green for hover
#     }

#     COMMON_FONT = ('Segoe UI', 12)
#     HEADER_FONT = ('Segoe UI', 32, 'bold')
    
#     # Window style - pitch black
#     root.configure(bg=COLORS['bg_dark'])

#     # Dark frame style
#     style.configure('Dark.TFrame',
#         background=COLORS['bg_dark'],
#         borderwidth=0)

#     # Title style
#     style.configure('Title.TLabel',
#         font=HEADER_FONT,
#         foreground=COLORS['primary'],
#         background=COLORS['bg_dark'])

#     # Regular labels
#     style.configure('TLabel',
#         font=COMMON_FONT,
#         foreground=COLORS['text'],
#         background=COLORS['bg_dark'])

#     # Entry style with dark background
#     style.configure('TEntry',
#         fieldbackground=COLORS['input_bg'],
#         foreground=COLORS['text'],
#         font=COMMON_FONT,
#         padding=10,
#         borderwidth=1,
#         relief='solid')

#     # Primary button - Neon green with black text
#     style.configure('Primary.TButton',
#         font=('Segoe UI', 12, 'bold'),
#         background=COLORS['primary'],
#         foreground=COLORS['text_dark'],
#         padding=(30, 15),
#         borderwidth=0)

#     style.map('Primary.TButton',
#         background=[('active', COLORS['hover'])])

#     # Link button - White text
#     style.configure('Link.TButton',
#         font=('Segoe UI', 10, 'underline'),
#         background=COLORS['bg_dark'],
#         foreground=COLORS['text'],
#         borderwidth=0,
#         padding=5)

#     style.map('Link.TButton',
#         background=[('active', COLORS['bg_dark'])],
#         foreground=[('active', COLORS['primary'])])

#     # Secondary button - Outlined neon
#     style.configure('Secondary.TButton',
#         font=('Segoe UI', 12, 'bold'),
#         background=COLORS['bg_dark'],
#         foreground=COLORS['primary'],
#         padding=(30, 15),
#         borderwidth=1,
#         relief='solid')

#     style.map('Secondary.TButton',
#         background=[('active', COLORS['primary'])],
#         foreground=[('active', COLORS['text_dark'])])

#     # Notebook with dark tabs
#     style.configure('TNotebook',
#         background=COLORS['bg_dark'],
#         borderwidth=0)

#     style.configure('TNotebook.Tab',
#         font=COMMON_FONT,
#         padding=(20, 10),
#         background=COLORS['bg_dark'],
#         foreground=COLORS['text'])

#     style.map('TNotebook.Tab',
#         background=[('selected', COLORS['primary'])],
#         foreground=[('selected', COLORS['text_dark'])])

#     # Treeview for password list
#     style.configure('Treeview',
#         background=COLORS['bg_dark'],
#         foreground=COLORS['text'],
#         fieldbackground=COLORS['bg_dark'],
#         font=COMMON_FONT)

#     style.configure('Treeview.Heading',
#         background=COLORS['primary'],
#         foreground=COLORS['text_dark'],
#         font=('Segoe UI', 10, 'bold'))

#     return style


#3rd edit
# import tkinter as tk
# from tkinter import messagebox, ttk
# import ttkbootstrap as tb

# class PasswordManagerApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Password Manager")
#         self.root.geometry("400x300")
#         self.root.configure(bg='#000000')  # Pure black background
        
#         # Apply theme
#         self.style = tb.Style(theme="darkly")
        
#         # Frame Styling
#         self.frame = ttk.Frame(self.root, padding=20, style='TFrame')
#         self.frame.pack(expand=True)
        
#         # Title Label
#         self.title_label = ttk.Label(self.frame, text="Password Manager", font=("Helvetica", 16, "bold"), foreground="#00FF00", background="#000000")
#         self.title_label.pack(pady=10)
        
#         # Buttons
#         self.add_button = ttk.Button(self.frame, text="Add Password", command=self.add_password, style='TButton')
#         self.add_button.pack(pady=5)
        
#         self.view_button = ttk.Button(self.frame, text="View Passwords", command=self.view_passwords, style='TButton')
#         self.view_button.pack(pady=5)
        
#         self.exit_button = ttk.Button(self.frame, text="Exit", command=self.root.quit, style='TButton')
#         self.exit_button.pack(pady=5)
        
#         # Button Styling
#         self.style.configure('TButton', font=("Helvetica", 12), background="#00FF00", foreground="#000000")
#         self.style.map('TButton', background=[('active', '#00CC00')])
    
#     def add_password(self):
#         add_window = tk.Toplevel(self.root)
#         add_window.title("Add Password")
#         add_window.geometry("300x250")
#         add_window.configure(bg='#000000')
        
#         ttk.Label(add_window, text="Website:", foreground="#00FF00", background="#000000").pack(pady=5)
#         website_entry = ttk.Entry(add_window)
#         website_entry.pack()
        
#         ttk.Label(add_window, text="Username:", foreground="#00FF00", background="#000000").pack(pady=5)
#         username_entry = ttk.Entry(add_window)
#         username_entry.pack()
        
#         ttk.Label(add_window, text="Password:", foreground="#00FF00", background="#000000").pack(pady=5)
#         password_entry = ttk.Entry(add_window, show='*')
#         password_entry.pack()
        
#         save_button = ttk.Button(add_window, text="Save", command=lambda: self.save_password(website_entry.get(), username_entry.get(), password_entry.get()), style='TButton')
#         save_button.pack(pady=10)
    
#     def save_password(self, website, username, password):
#         if website and username and password:
#             with open("passwords.txt", "a") as file:
#                 file.write(f"{website} | {username} | {password}\n")
#             messagebox.showinfo("Success", "Password Saved!")
#         else:
#             messagebox.showwarning("Error", "All fields are required!")
    
#     def view_passwords(self):
#         view_window = tk.Toplevel(self.root)
#         view_window.title("Stored Passwords")
#         view_window.geometry("400x300")
#         view_window.configure(bg='#000000')
        
#         try:
#             with open("passwords.txt", "r") as file:
#                 passwords = file.readlines()
#                 if passwords:
#                     text_area = tk.Text(view_window, wrap=tk.WORD, bg="#000000", fg="#00FF00", font=("Helvetica", 10))
#                     text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)
#                     text_area.insert(tk.END, "".join(passwords))
#                     text_area.config(state=tk.DISABLED)
#                 else:
#                     ttk.Label(view_window, text="No saved passwords.", foreground="#00FF00", background="#000000").pack(pady=20)
#         except FileNotFoundError:
#             ttk.Label(view_window, text="No saved passwords.", foreground="#00FF00", background="#000000").pack(pady=20)

# if __name__ == "__main__":
#     root = tk.Tk()
#     app = PasswordManagerApp(root)
#     root.mainloop()


#4th edit

import ttkbootstrap as ttk

def apply_styles(root):
    style = ttk.Style()
    style.theme_use('darkly')

    COLORS = {
        'primary': '#1DD75B',          # GUI's neon green
        'bg_dark': '#171A1F',          # GUI's dark background
        'text': '#000000',             # Black text for buttons
        'text_light': '#FFFFFF',       # White text
        'hover': '#32CD32',            # Hover green
    }

    FONTS = {
        'title': ('Archivo', 32),
        'button': ('Archivo', 14, 'bold'),
        'input': ('Archivo', 12),
    }

    # Window style
    root.configure(bg=COLORS['bg_dark'])

    # Frame style
    style.configure('TFrame',
        background=COLORS['bg_dark'])

    # Label style
    style.configure('TLabel',
        font=FONTS['input'],
        foreground=COLORS['primary'],
        background=COLORS['bg_dark'])

    # Title label style
    style.configure('Title.TLabel',
        font=FONTS['title'],
        foreground=COLORS['primary'],
        background=COLORS['bg_dark'])

    # Entry style
    style.configure('TEntry',
        fieldbackground=COLORS['bg_dark'],
        foreground=COLORS['primary'],
        insertcolor=COLORS['primary'],
        font=FONTS['input'],
        borderwidth=2,
        relief='solid')

    # Button style
    style.configure('TButton',
        font=FONTS['button'],
        background=COLORS['primary'],
        foreground=COLORS['text'],
        borderwidth=0,
        relief='flat')

    style.map('TButton',
        background=[('active', COLORS['hover'])])

    # Link button style
    style.configure('Link.TButton',
        font=FONTS['input'],
        background=COLORS['bg_dark'],
        foreground=COLORS['primary'],
        borderwidth=0,
        relief='flat')

    return style