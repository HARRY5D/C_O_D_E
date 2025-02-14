# Add Supabase client
from supabase import create_client, Client
import os
from dotenv import load_dotenv

load_dotenv()
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Add styling constants
GITHUB_COLORS = {
    'bg': '#0d1117',
    'fg': '#c9d1d9',
    'button': '#238636',
    'button_hover': '#2ea043',
    'input_bg': '#21262d',
    'border': '#30363d'
}

class PasswordManagerApp:
    def __init__(self):
        # ...existing code...
        self.setup_styles()
        
    def setup_styles(self):
        style = ttk.Style()
        style.configure('Github.TButton',
            background=GITHUB_COLORS['button'],
            foreground=GITHUB_COLORS['fg'],
            padding=10)
        style.configure('Github.TEntry',
            fieldbackground=GITHUB_COLORS['input_bg'],
            foreground=GITHUB_COLORS['fg'])
            
    def create_login_window(self):
        self.clear_window()
        self.root.configure(bg=GITHUB_COLORS['bg'])
        
        frame = ttk.Frame(self.root, style='Github.TFrame')
        frame.pack(pady=20, padx=20)
        
        ttk.Label(frame, text="Username:", style='Github.TLabel').pack()
        self.username_entry = ttk.Entry(frame, style='Github.TEntry')
        self.username_entry.pack()
        
        ttk.Label(frame, text="Password:", style='Github.TLabel').pack()
        self.password_entry = ttk.Entry(frame, show="*", style='Github.TEntry')
        self.password_entry.pack()
        
        ttk.Button(frame, text="Login", command=self.login, style='Github.TButton').pack(pady=5)
        ttk.Button(frame, text="Register", command=self.create_registration_window, 
                  style='Github.TButton').pack(pady=5)
        ttk.Button(frame, text="Forgot Password?", command=self.forgot_password, 
                  style='Github.TButton').pack(pady=5)

    def forgot_password(self):
        self.clear_window()
        
        frame = ttk.Frame(self.root, style='Github.TFrame')
        frame.pack(pady=20, padx=20)
        
        ttk.Label(frame, text="Email:", style='Github.TLabel').pack()
        self.reset_email = ttk.Entry(frame, style='Github.TEntry')
        self.reset_email.pack()
        
        ttk.Button(frame, text="Reset Password", command=self.send_reset_email, 
                  style='Github.TButton').pack(pady=5)
        ttk.Button(frame, text="Back", command=self.create_login_window, 
                  style='Github.TButton').pack(pady=5)

    async def send_reset_email(self):
        email = self.reset_email.get()
        try:
            data = await supabase.auth.reset_password_email(email)
            messagebox.showinfo("Success", 
                "Password reset instructions have been sent to your email")
            self.create_login_window()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    async def verify_reset_token(self, token):
        try:
            data = await supabase.auth.verify_password_reset(token)
            return True
        except Exception:
            return False