import sys
import os
from PyQt6.QtWidgets import QApplication
from ui.login_window import LoginWindow
from ui.main_window import MainWindow
from encryption import Encryptor
from database.database_manager import DatabaseManager
import uuid
import string
import secrets
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Email configuration
SENDER_EMAIL = "sgp.noreplydce@gmail.com"
SENDER_PASSWORD = "haub ylen jpof ypse"

# Define dark theme colors for consistency
BACKGROUND_COLOR = "#1e1e1e"  # Darker background for all windows
FOREGROUND_COLOR = "#ffffff"
BUTTON_BACKGROUND = "#333333"
ENTRY_BACKGROUND = "#2e2e2e"
ACCENT_COLOR = "#4a6984"
SELECTED_COLOR = "#5a7994"
HOVER_COLOR = "#3a5066"

class PasswordManager:
    def __init__(self):
        self.app = QApplication(sys.argv)
        
        # Set application-wide dark style
        self.apply_dark_theme()
        
        # Create app data directory if it doesn't exist
        self.app_data_dir = os.path.join(os.path.expanduser('~'), 'PyLock')
        os.makedirs(self.app_data_dir, exist_ok=True)
        
        # Initialize database
        db_path = os.path.join(self.app_data_dir, 'pylock.db')
        self.db = DatabaseManager(db_path)
        
        self.encryptor = Encryptor()
        self.current_key = None
        self.user_id = str(uuid.uuid4())
        
        self.login_window = LoginWindow()
        self.main_window = MainWindow()
        
        # Connect signals
        self.login_window.login_successful.connect(self.handle_login)
        self.login_window.request_verification.connect(self.send_verification_code)
        
        # Connect main window signals to database functions
        self.main_window.password_added.connect(self.save_password)
        self.main_window.password_edited.connect(self.update_password)
        self.main_window.password_deleted.connect(self.delete_password)
        self.main_window.password_generation_requested.connect(self.generate_password)
        
        self.login_window.show()
        
    def apply_dark_theme(self):
        """Apply dark theme to the entire application"""
        # Set application style sheet
        dark_stylesheet = f"""
        QWidget {{
            background-color: {BACKGROUND_COLOR};
            color: {FOREGROUND_COLOR};
        }}
        
        QPushButton {{
            background-color: {BUTTON_BACKGROUND};
            border: 1px solid #555;
            border-radius: 3px;
            padding: 5px;
            min-width: 80px;
        }}
        
        QPushButton:hover {{
            background-color: {ACCENT_COLOR};
        }}
        
        QPushButton:pressed {{
            background-color: {HOVER_COLOR};
        }}
        
        QLineEdit, QTextEdit, QPlainTextEdit, QComboBox {{
            background-color: {ENTRY_BACKGROUND};
            border: 1px solid #555;
            border-radius: 2px;
            padding: 3px;
            color: {FOREGROUND_COLOR};
        }}
        
        QTabWidget::pane {{
            border: 1px solid #555;
        }}
        
        QTabBar::tab {{
            background-color: {BUTTON_BACKGROUND};
            color: {FOREGROUND_COLOR};
            padding: 6px 12px;
            margin-right: 2px;
        }}
        
        QTabBar::tab:selected {{
            background-color: {ACCENT_COLOR};
        }}
        
        QTabBar::tab:hover:!selected {{
            background-color: {HOVER_COLOR};
        }}
        
        QMenu {{
            background-color: {BACKGROUND_COLOR};
            border: 1px solid #555;
        }}
        
        QMenu::item {{
            padding: 5px 20px;
        }}
        
        QMenu::item:selected {{
            background-color: {ACCENT_COLOR};
        }}
        
        QTableView {{
            background-color: {ENTRY_BACKGROUND};
            alternate-background-color: #252525;
            selection-background-color: {ACCENT_COLOR};
        }}
        
        QHeaderView::section {{
            background-color: {BUTTON_BACKGROUND};
            padding: 4px;
            border: 1px solid #555;
        }}
        
        QScrollBar {{
            background-color: {BUTTON_BACKGROUND};
        }}
        
        QScrollBar::handle {{
            background-color: #666;
            border-radius: 4px;
        }}
        
        QScrollBar::handle:hover {{
            background-color: #888;
        }}
        """
        
        self.app.setStyleSheet(dark_stylesheet)

    def handle_login(self, master_password):
        # Generate encryption key from master password
        key = self.encryptor.generate_key(master_password)
        self.current_key = key
        
        # Save/verify user data
        user_data = self.db.get_user(self.user_id)
        if user_data is None:
            # New user - save the salt and key hash
            special_sentence = self.generate_special_sentence()
            self.db.save_user(self.user_id, str(key), self.encryptor.get_salt(), special_sentence)
        
        # Load existing passwords
        self.load_passwords()
        
        # Switch to main window
        self.login_window.hide()
        self.main_window.show()

    def load_passwords(self):
        passwords = self.db.get_all_passwords(self.user_id)
        for pwd in passwords:
            try:
                decrypted_password = self.encryptor.decrypt_data(
                    pwd['encrypted_password'], 
                    self.current_key
                )
                self.main_window.add_password_to_table({
                    'id': pwd['id'],
                    'title': pwd['title'],
                    'username': pwd['username'],
                    'password': decrypted_password,
                    'url': pwd['url'],
                    'notes': pwd['notes']
                })
            except Exception as e:
                print(f"Error decrypting password: {e}")

    def save_password(self, password_data):
        # Check if same username exists for this service
        existing = self.db.check_duplicate_username(
            self.user_id,
            password_data['title'],
            password_data['username']
        )
        
        if existing and not password_data.get('edit_mode', False):
            self.main_window.show_error(
                f"Username '{password_data['username']}' already exists for service '{password_data['title']}'. "
                "Please use a different username."
            )
            return False

        encrypted_pwd = self.encryptor.encrypt_data(password_data['password'], self.current_key)
        
        if password_data.get('edit_mode', False) and password_data.get('id'):
            # Update existing password
            self.update_password(password_data['id'], password_data)
        else:
            # Create new password entry
            password_id = self.db.save_password(
                self.user_id,
                password_data['title'],
                password_data['username'],
                encrypted_pwd,
                password_data['url'],
                password_data['notes']
            )
            return password_id
        
        return True

    def update_password(self, password_id, password_data):
        encrypted_pwd = self.encryptor.encrypt_data(password_data['password'], self.current_key)
        
        # Check for username conflicts when updating
        if self.db.check_duplicate_username_except(
            self.user_id,
            password_data['title'],
            password_data['username'],
            password_id
        ):
            self.main_window.show_error(
                f"Another account with username '{password_data['username']}' "
                f"already exists for service '{password_data['title']}'"
            )
            return False
            
        success = self.db.update_password(
            password_id,
            password_data['title'],
            password_data['username'],
            encrypted_pwd,
            password_data['url'],
            password_data['notes']
        )
        return success

    def delete_password(self, password_id):
        return self.db.delete_password(password_id)
    
    def delete_password_by_service_username(self, service, username):
        """Delete a specific password entry by service name and username"""
        return self.db.delete_password_by_criteria(
            self.user_id, service, username
        )
    
    def generate_password(self, length=16, include_uppercase=True, include_digits=True, include_special=True):
        """Generate a secure random password"""
        chars = string.ascii_lowercase
        if include_uppercase:
            chars += string.ascii_uppercase
        if include_digits:
            chars += string.digits
        if include_special:
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
            
        password = "".join(secrets.choice(chars) for _ in range(length))
        return password
    
    def generate_special_sentence(self):
        """Generate a special sentence for account recovery"""
        word_lists = [
            ["apple", "banana", "cherry", "date", "blueberry", "fig", "grape"],
            ["elephant", "tiger", "dolphin", "eagle", "penguin", "koala", "panda"],
            ["red", "green", "blue", "yellow", "purple", "orange", "teal"],
            ["sunny", "rainy", "cloudy", "snowy", "windy", "stormy", "foggy"]
        ]
        special_words = [secrets.choice(category) for category in word_lists]
        special_words += [secrets.choice(secrets.choice(word_lists)) for _ in range(2)]
        secrets.SystemRandom().shuffle(special_words)
        return " ".join(special_words)
    
    def generate_verification_code(self):
        """Generate a 6-digit verification code for 2FA"""
        return "".join(secrets.choice(string.digits) for _ in range(6))
    
    def send_verification_code(self, email):
        """Send verification code via email for 2FA"""
        verification_code = self.generate_verification_code()
        
        subject = "PyLock Desktop Verification Code"
        body = f"""
        Your verification code is: {verification_code}
        
        Please enter this code to verify your login.
        If you did not request this code, please ignore this email.
        """
        
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))
        
        try:
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            # Store verification code in database for later verification
            self.db.save_verification_code(self.user_id, verification_code)
            
            return True
        except Exception as e:
            print(f"Failed to send verification email: {e}")
            return False

    def run(self):
        return self.app.exec()

if __name__ == '__main__':
    manager = PasswordManager()
    sys.exit(manager.run())