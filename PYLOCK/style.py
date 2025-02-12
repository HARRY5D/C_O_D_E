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


import ttkbootstrap as ttk
from ttkbootstrap.constants import *

def apply_styles(root):
    # Define the color palette
    COLORS = {
        'primary': '#39FF14',  # Neon green
        'secondary': '#1F1F1F',  # Dark gray
        'bg_dark': '#000000',  # Pure black
        'bg_light': '#0A0A0A',  # Slightly lighter black
        'text': '#FFFFFF',  # White text
        'input_bg': '#121212',  # Dark input background
        'border': '#39FF14',  # Neon green border
        'error': '#FF0033',  # Bright red
        'hover': '#32CD32'  # Lighter green for hover
    }

    # Set theme to 'darkly' for a modern look
    style = ttk.Style()
    style.theme_use('darkly')

    # Apply background color to main window
    root.configure(bg=COLORS['bg_dark'])

    # Fonts
    COMMON_FONT = ('Segoe UI', 10)
    HEADER_FONT = ('Segoe UI', 24, 'bold')

    # Labels
    style.configure('TLabel',
        font=COMMON_FONT,
        foreground=COLORS['text'],
        background=COLORS['bg_dark'])

    style.configure('Header.TLabel',
        font=HEADER_FONT,
        foreground=COLORS['primary'],
        background=COLORS['bg_dark'])

    # Entry Fields
    style.configure('TEntry',
        fieldbackground=COLORS['input_bg'],
        foreground=COLORS['text'],
        insertcolor=COLORS['primary'],
        font=COMMON_FONT,
        padding=10,
        borderwidth=2,
        relief='solid')

    # Primary Button (Neon Green)
    style.configure('Primary.TButton',
        font=('Segoe UI', 12, 'bold'),
        background=COLORS['primary'],
        foreground=COLORS['bg_dark'],
        padding=(20, 10),
        borderwidth=0)

    style.map('Primary.TButton',
        background=[('active', COLORS['hover'])],
        foreground=[('active', COLORS['bg_dark'])])

    # Secondary Button (Dark Gray)
    style.configure('Secondary.TButton',
        font=('Segoe UI', 12, 'bold'),
        background=COLORS['secondary'],
        foreground=COLORS['primary'],
        padding=(20, 10),
        borderwidth=2,
        relief='solid')

    style.map('Secondary.TButton',
        background=[('active', COLORS['bg_light'])],
        foreground=[('active', COLORS['primary'])])

    # Error Button (Red)
    style.configure('Danger.TButton',
        font=('Segoe UI', 12, 'bold'),
        background=COLORS['error'],
        foreground=COLORS['text'],
        padding=(20, 10),
        borderwidth=0)

    # Frames with neon border
    style.configure('TFrame',
        background=COLORS['bg_dark'],
        borderwidth=2,
        relief='solid')

    # Notebook (Tabs)
    style.configure('TNotebook',
        background=COLORS['bg_dark'],
        borderwidth=0)

    style.configure('TNotebook.Tab',
        font=('Segoe UI', 11, 'bold'),
        padding=(15, 8),
        background=COLORS['bg_light'],
        foreground=COLORS['primary'])

    style.map('TNotebook.Tab',
        background=[('selected', COLORS['bg_dark'])],
        foreground=[('selected', COLORS['primary'])])

    # Labels for sections
    style.configure('Title.TLabel',
        font=('Segoe UI', 32, 'bold'),
        foreground=COLORS['primary'],
        background=COLORS['bg_dark'])

    style.configure('Subtitle.TLabel',
        font=('Segoe UI', 14),
        foreground=COLORS['text'],
        background=COLORS['bg_dark'])

    # LabelFrame (for grouping)
    style.configure('TLabelframe',
        background=COLORS['bg_dark'],
        foreground=COLORS['primary'],
        bordercolor=COLORS['border'])

    style.configure('TLabelframe.Label',
        font=('Segoe UI', 11, 'bold'),
        foreground=COLORS['primary'],
        background=COLORS['bg_dark'])

    # Treeview (Tables)
    style.configure('Treeview',
        background=COLORS['bg_dark'],
        foreground=COLORS['text'],
        fieldbackground=COLORS['bg_dark'])

    style.configure('Treeview.Heading',
        background=COLORS['secondary'],
        foreground=COLORS['primary'],
        font=('Segoe UI', 10, 'bold'))

    # Canvas (for graphs, charts, etc.)
    style.configure('TCanvas',
        background=COLORS['bg_dark'],
        borderwidth=0,
        relief='flat')

    return style
