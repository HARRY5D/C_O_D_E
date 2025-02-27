# import tkinter as tk
# import ttkbootstrap as ttk
# from tkinter import messagebox
# import sqlite3
# #import hashlib
# import os
# import secrets
# import string
# from cryptography.hazmat.primitives import hashes
# from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
# from cryptography.hazmat.backends import default_backend
# from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
# import base64
# from style import apply_styles

# backend = default_backend()


# class DatabaseManager:
#     def __init__(self):
#         self.conn = sqlite3.connect('passwords.db')
#         self.create_tables()

#     def create_tables(self):
#         cursor = self.conn.cursor()
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS users (
#                 id INTEGER PRIMARY KEY,
#                 username TEXT UNIQUE,
#                 password_hash TEXT,
#                 salt TEXT,
#                 email TEXT,
#                 phone TEXT,
#                 verified INTEGER DEFAULT 0
#             )
#         ''')
#         cursor.execute('''
#             CREATE TABLE IF NOT EXISTS passwords (
#                 id INTEGER PRIMARY KEY,
#                 user_id INTEGER,
#                 service TEXT,
#                 username TEXT,
#                 password TEXT,
#                 iv TEXT,
#                 FOREIGN KEY(user_id) REFERENCES users(id)
#             )
#         ''')
#         self.conn.commit()

#     def execute_query(self, query, params=()):
#         cursor = self.conn.cursor()
#         cursor.execute(query, params)
#         self.conn.commit()
#         return cursor


# class AuthManager:
#     @staticmethod
#     def hash_password(password, salt=None):
#         salt = salt or os.urandom(16)
#         kdf = PBKDF2HMAC(
#             algorithm=hashes.SHA256(),
#             length=32,
#             salt=salt,
#             iterations=100000,
#             backend=backend
#         )
#         key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
#         return key.decode(), salt.hex()

#     @staticmethod
#     def generate_verification_code():
#         return ''.join(secrets.choice(string.digits) for _ in range(6))


# class EncryptionManager:
#     @staticmethod
#     def encrypt_password(password, master_key):
#         iv = os.urandom(16)
#         cipher = Cipher(algorithms.AES(master_key), modes.CFB(iv), backend=backend)
#         encryptor = cipher.encryptor()
#         ct = encryptor.update(password.encode()) + encryptor.finalize()
#         return base64.urlsafe_b64encode(ct).decode(), iv.hex()

#     @staticmethod
#     def decrypt_password(encrypted_password, iv, master_key):
#         iv = bytes.fromhex(iv)
#         ct = base64.urlsafe_b64decode(encrypted_password)
#         cipher = Cipher(algorithms.AES(master_key), modes.CFB(iv), backend=backend)
#         decryptor = cipher.decryptor()
#         return (decryptor.update(ct) + decryptor.finalize()).decode()


# # class PasswordManagerApp:
# #     def __init__(self):
# #         self.db = DatabaseManager()
# #         self.current_user = None
# #         self.master_key = None

# #         # self.root = tk.Tk()
# #         # self.root.title("Password Manager")
# #         # self.create_login_window()
# #         # self.root.mainloop()
# #         self.root = ttk.Window(themename="darkly")
# #         self.root.title("PyLock Password Manager")
# #         self.root.geometry("800x600")
# #         self.create_login_window()
# #         self.root.mainloop()

# #     def create_login_window(self):
# #         self.clear_window()

# #         ttk.Label(self.root, text="Username:").pack()
# #         self.username_entry = ttk.Entry(self.root)
# #         self.username_entry.pack()

# #         ttk.Label(self.root, text="Password:").pack()
# #         self.password_entry = ttk.Entry(self.root, show="*")
# #         self.password_entry.pack()

# #         ttk.Button(self.root, text="Login", command=self.login).pack(pady=5)
# #         ttk.Button(self.root, text="Register", command=self.create_registration_window).pack(pady=5)

# class PasswordManagerApp:
#     def __init__(self):
#         self.db = DatabaseManager()
#         self.current_user = None
#         self.master_key = None

#         self.root = ttk.Window(themename="darkly")
#         self.root.title("PyLock Password Manager")
#         self.root.geometry("1440x900")
#         self.style = apply_styles(self.root)
#         self.create_login_window()
#         self.root.mainloop()

#     def create_login_window(self):
#         self.clear_window()
#         #increased y by  20
#         # Title
#         ttk.Label(
#             self.root, 
#             text="PyLock", 
#             style="Title.TLabel"
#         ).place(x=14, y=9)

#         # Username section
#         ttk.Label(
#             self.root, 
#             text="Enter username:", 
#             style="Title.TLabel"
#         ).place(x=602, y=134)
        
#         self.username_entry = ttk.Entry(self.root, width=30)
#         self.username_entry.place(x=607, y=210, width=248, height=49)

#         # Password section
#         ttk.Label(
#             self.root, 
#             text="Enter password:", 
#             style="Title.TLabel"
#         ).place(x=610, y=292)
        
#         self.password_entry = ttk.Entry(self.root,show="•", width=30)
#         self.password_entry.place(x=607, y=370, width=248, height=49)

#         # Sign in button
#         ttk.Button(
#             self.root,
#             text="Sign In",
#             command=self.login
#         ).place(x=607, y=456, width=248, height=47)

#         # Register link
#         ttk.Button(
#             self.root,
#             text="Create Account",
#             style="Link.TButton",
#             command=self.create_registration_window
#         ).place(x=607, y=520)

#     def create_registration_window(self):
#         self.clear_window()
        
#         # Title
#         ttk.Label(
#             self.root, 
#             text="Create Account", 
#             style="Title.TLabel"
#         ).place(x=602, y=50)

#         # Registration fields with consistent spacing
#         # fields = [
#         #     ("Username", self.reg_username := ttk.Entry(self.root, width=30)),
#         #     ("Password", self.reg_password := ttk.Entry(self.root, width=30, show="•")),
#         #     ("Email", self.reg_email := ttk.Entry(self.root, width=30)),
#         #     ("Phone", self.reg_phone := ttk.Entry(self.root, width=30))
#         # ]
#                 # Create entries first
#         self.reg_username = ttk.Entry(self.root, width=30)
#         self.reg_password = ttk.Entry(self.root, width=30, show="•")
#         self.reg_email = ttk.Entry(self.root, width=30)
#         self.reg_phone = ttk.Entry(self.root, width=30)

#         # Then create fields list
#         fields = [
#             ("Username", self.reg_username),
#             ("Password", self.reg_password),
#             ("Email", self.reg_email),
#             ("Phone", self.reg_phone)
#         ]
        

#         y_pos = 150
#         for label_text, entry in fields:
#             ttk.Label(
#                 self.root, 
#                 text=label_text, 
#                 style="TLabel"
#             ).place(x=607, y=y_pos)
            
#             entry.place(x=607, y=y_pos + 40, width=248, height=49)
#             y_pos += 120

#         # Buttons
#         ttk.Button(
#             self.root,
#             text="Register",
#             command=self.register
#         ).place(x=607, y=y_pos, width=248, height=47)

#         ttk.Button(
#             self.root,
#             text="Back to Login",
#             style="Link.TButton",
#             command=self.create_login_window
#         ).place(x=607, y=y_pos + 64)

#     # ... rest of the methods remain the same ...
    
#     # def create_registration_window(self):
#     #     self.clear_window()

#     #     ttk.Label(self.root, text="Choose a username:").pack()
#     #     self.reg_username = ttk.Entry(self.root)
#     #     self.reg_username.pack()

#     #     ttk.Label(self.root, text="Choose a password:").pack()
#     #     self.reg_password = ttk.Entry(self.root, show="*")
#     #     self.reg_password.pack()

#     #     ttk.Label(self.root, text="Email:").pack()
#     #     self.reg_email = ttk.Entry(self.root)
#     #     self.reg_email.pack()

#     #     ttk.Label(self.root, text="Phone:").pack()
#     #     self.reg_phone = ttk.Entry(self.root)
#     #     self.reg_phone.pack()

#     #     ttk.Button(self.root, text="Register", command=self.register).pack(pady=5)
#     #     ttk.Button(self.root, text="Back", command=self.create_login_window).pack(pady=5)

#     def create_main_window(self):
#         self.clear_window()

#         notebook = ttk.Notebook(self.root)

#         # Add Password Tab
#         add_frame = ttk.Frame(notebook)
#         ttk.Label(add_frame, text="Service:").pack()
#         self.service_entry = ttk.Entry(add_frame)
#         self.service_entry.pack()

#         ttk.Label(add_frame, text="Username:").pack()
#         self.account_user_entry = ttk.Entry(add_frame)
#         self.account_user_entry.pack()

#         ttk.Label(add_frame, text="Password:").pack()
#         self.account_pass_entry = ttk.Entry(add_frame, show="*")
#         self.account_pass_entry.pack()

#         ttk.Button(add_frame, text="Generate Password", command=self.generate_password).pack(pady=5)
#         ttk.Button(add_frame, text="Save", command=self.save_password).pack(pady=5)

#         # Retrieve Password Tab
#         retrieve_frame = ttk.Frame(notebook)
#         ttk.Label(retrieve_frame, text="Service:").pack()
#         self.retrieve_service = ttk.Entry(retrieve_frame)
#         self.retrieve_service.pack()

#         ttk.Button(retrieve_frame, text="Retrieve", command=self.retrieve_password).pack(pady=5)
#         self.retrieve_result = ttk.Label(retrieve_frame, text="")
#         self.retrieve_result.pack()

#         notebook.add(add_frame, text="Add Password")
#         notebook.add(retrieve_frame, text="Retrieve Password")
#         notebook.pack(expand=True, fill="both")

#         ttk.Button(self.root, text="Logout", command=self.logout).pack(pady=5)

#     def generate_password(self):
#         chars = string.ascii_letters + string.digits + "!@#$%^&*()"
#         password = ''.join(secrets.choice(chars) for _ in range(16))
#         self.account_pass_entry.delete(0, tk.END)
#         self.account_pass_entry.insert(0, password)

#     def save_password(self):
#         if not self.current_user:
#             messagebox.showerror("Error", "Please log in first")
#             return

#         service = self.service_entry.get()
#         username = self.account_user_entry.get()
#         password = self.account_pass_entry.get()

#         encrypted_password, iv = EncryptionManager.encrypt_password(password, self.master_key)

#         self.db.execute_query('''
#             INSERT INTO passwords (user_id, service, username, password, iv)
#             VALUES (?, ?, ?, ?, ?)
#         ''', (self.current_user[0], service, username, encrypted_password, iv))

#         messagebox.showinfo("Success", "Password saved successfully")

#     def retrieve_password(self):
#         if not self.current_user:
#             messagebox.showerror("Error", "Please log in first")
#             return
            
#         service = self.retrieve_service.get()
#         result = self.db.execute_query('''
#             SELECT username, password, iv FROM passwords
#             WHERE user_id = ? AND service = ?
#         ''', (self.current_user[0], service)).fetchone()

#         if result:
#             username, encrypted_password, iv = result
#             decrypted_password = EncryptionManager.decrypt_password(
#                 encrypted_password, iv, self.master_key
#             )
#             self.retrieve_result.config(text=f"Username: {username}\nPassword: {decrypted_password}")
#         else:
#             messagebox.showerror("Error", "No password found for this service")

#     def login(self):
#         username = self.username_entry.get()
#         password = self.password_entry.get()

#         user = self.db.execute_query('''
#             SELECT id, password_hash, salt FROM users WHERE username = ?
#         ''', (username,)).fetchone()

#         if user:
#             stored_key = user[1]
#             salt = bytes.fromhex(user[2])
#             derived_key, _ = AuthManager.hash_password(password, salt)

#             if derived_key == stored_key:
#                 self.current_user = user
#                 self.master_key = base64.urlsafe_b64decode(derived_key)
#                 self.create_main_window()
#                 return

#         messagebox.showerror("Error", "Invalid credentials")

#     def register(self):
#         username = self.reg_username.get()
#         password = self.reg_password.get()
#         email = self.reg_email.get()
#         phone = self.reg_phone.get()

#         if not all([username, password, email, phone]):
#             messagebox.showerror("Error", "All fields are required")
#             return

#         derived_key, salt = AuthManager.hash_password(password)

#         try:
#             self.db.execute_query('''
#                 INSERT INTO users (username, password_hash, salt, email, phone)
#                 VALUES (?, ?, ?, ?, ?)
#             ''', (username, derived_key, salt, email, phone))

#             messagebox.showinfo("Success", "Registration successful! Please verify your account.")
#             self.create_login_window()
#         except sqlite3.IntegrityError:
#             messagebox.showerror("Error", "Username already exists")

#     def logout(self):
#         self.current_user = None
#         self.master_key = None
#         self.create_login_window()

#     def clear_window(self):
#         for widget in self.root.winfo_children():
#             widget.destroy()


# if __name__ == "__main__":
#     PasswordManagerApp()