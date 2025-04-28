from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QPushButton, 
    QVBoxLayout, QHBoxLayout, QWidget, QMessageBox,
    QDialog, QFormLayout, QCheckBox
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QIcon

class VerificationDialog(QDialog):
    verification_complete = pyqtSignal(bool)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Verification")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Instructions
        info_label = QLabel("Please enter the verification code sent to your email:")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Code input
        self.code_input = QLineEdit()
        self.code_input.setPlaceholderText("Enter 6-digit code")
        self.code_input.setMaxLength(6)
        self.code_input.setFont(QFont("Arial", 16))
        self.code_input.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.code_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.verify_button = QPushButton("Verify")
        self.verify_button.clicked.connect(self.accept)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        self.resend_button = QPushButton("Resend Code")
        self.resend_button.clicked.connect(self.resend_code)
        
        button_layout.addWidget(self.resend_button)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.verify_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def get_verification_code(self):
        return self.code_input.text()
    
    def resend_code(self):
        self.verification_complete.emit(False)

class EmailInputDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Email Verification")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        
        # Instructions
        info_label = QLabel("Enter your email address to receive a verification code:")
        info_label.setWordWrap(True)
        layout.addWidget(info_label)
        
        # Email input
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email address")
        layout.addWidget(self.email_input)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.send_button = QPushButton("Send Code")
        self.send_button.clicked.connect(self.accept)
        
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.send_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
    
    def get_email(self):
        return self.email_input.text()

class LoginWindow(QMainWindow):
    login_successful = pyqtSignal(str)
    request_verification = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyLock - Login")
        self.setMinimumSize(500, 350)
        
        # Central widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Title label
        title_label = QLabel("PyLock")
        title_label.setFont(QFont("Arial", 24, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Secure Password Manager")
        subtitle_label.setFont(QFont("Arial", 12))
        subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(subtitle_label)
        
        main_layout.addSpacing(20)
        
        # Form layout for inputs
        form_layout = QFormLayout()
        
        # Password input
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter master password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addRow("Master Password:", self.password_input)
        
        # Remember me checkbox
        self.remember_me = QCheckBox("Remember me on this device")
        form_layout.addRow("", self.remember_me)
        
        # Two-factor authentication checkbox
        self.use_2fa = QCheckBox("Use 2FA (Email verification)")
        form_layout.addRow("", self.use_2fa)
        
        main_layout.addLayout(form_layout)
        
        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        main_layout.addWidget(self.login_button)
        
        # Forgot password button
        self.forgot_button = QPushButton("Forgot Password")
        self.forgot_button.clicked.connect(self.handle_forgot_password)
        main_layout.addWidget(self.forgot_button)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Set up event handlers
        self.password_input.returnPressed.connect(self.handle_login)
        
    def handle_login(self):
        password = self.password_input.text()
        
        if not password:
            QMessageBox.warning(self, "Error", "Please enter a master password")
            return
            
        # If 2FA is enabled, initiate verification process
        if self.use_2fa.isChecked():
            self.initiate_2fa(password)
        else:
            # Direct login without 2FA
            self.login_successful.emit(password)
    
    def initiate_2fa(self, password):
        # First get the email address
        email_dialog = EmailInputDialog(self)
        if email_dialog.exec():
            email = email_dialog.get_email()
            
            # Basic email validation
            if not email or '@' not in email:
                QMessageBox.warning(self, "Error", "Please enter a valid email address")
                return
            
            # Request verification code to be sent
            self.request_verification.emit(email)
            
            # Show verification dialog
            verification_dialog = VerificationDialog(self)
            verification_dialog.verification_complete.connect(
                lambda resend: self.request_verification.emit(email) if resend else None
            )
            
            if verification_dialog.exec():
                verification_code = verification_dialog.get_verification_code()
                
                # Here we would normally verify the code against the stored one
                # For now, we'll just emit login_successful
                self.login_successful.emit(password)
            else:
                QMessageBox.information(self, "Canceled", "Verification was canceled")
    
    def handle_forgot_password(self):
        QMessageBox.information(
            self,
            "Forgot Password",
            "Please use your recovery sentence to reset your password.\n\n"
            "If you don't have your recovery sentence, you will need to create a new vault."
        )
        # Additional recovery flow can be added here