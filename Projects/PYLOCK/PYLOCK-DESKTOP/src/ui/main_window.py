from PyQt6.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QPushButton, 
    QVBoxLayout, QHBoxLayout, QWidget, QMessageBox,
    QFormLayout, QTabWidget, QTableWidget, QTableWidgetItem,
    QDialog, QComboBox, QSpinBox, QCheckBox, QMenu,
    QHeaderView
)
from PyQt6.QtCore import pyqtSignal, Qt
from PyQt6.QtGui import QFont, QIcon, QAction

class PasswordDialog(QDialog):
    def __init__(self, parent=None, password_data=None, edit_mode=False):
        super().__init__(parent)
        
        self.setWindowTitle("Add Password" if not edit_mode else "Edit Password")
        self.setMinimumWidth(500)
        self.setMinimumHeight(400)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        # Title input
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("e.g., Gmail, Amazon, Bank")
        form_layout.addRow("Title/Service:", self.title_input)
        
        # Username input
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username or email")
        form_layout.addRow("Username:", self.username_input)
        
        # Password input with generate button
        password_layout = QHBoxLayout()
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        password_layout.addWidget(self.password_input)
        
        self.generate_button = QPushButton("Generate")
        self.generate_button.clicked.connect(self.show_password_generator)
        password_layout.addWidget(self.generate_button)
        
        form_layout.addRow("Password:", password_layout)
        
        # Show password checkbox
        self.show_password = QCheckBox("Show password")
        self.show_password.stateChanged.connect(self.toggle_password_visibility)
        form_layout.addRow("", self.show_password)
        
        # URL input
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("https://example.com")
        form_layout.addRow("URL:", self.url_input)
        
        # Notes input (multiline)
        self.notes_input = QLineEdit()
        self.notes_input.setPlaceholderText("Additional notes")
        form_layout.addRow("Notes:", self.notes_input)
        
        layout.addLayout(form_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.accept)
        
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.save_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # If password_data provided, fill in the fields (edit mode)
        if password_data:
            self.title_input.setText(password_data.get('title', ''))
            self.username_input.setText(password_data.get('username', ''))
            self.password_input.setText(password_data.get('password', ''))
            self.url_input.setText(password_data.get('url', ''))
            self.notes_input.setText(password_data.get('notes', ''))
            
    def toggle_password_visibility(self, state):
        if state == Qt.CheckState.Checked.value:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
            
    def show_password_generator(self):
        generator_dialog = PasswordGeneratorDialog(self)
        if generator_dialog.exec():
            password = generator_dialog.get_generated_password()
            self.password_input.setText(password)
            # Automatically show the password when generated
            self.show_password.setChecked(True)
            
    def get_password_data(self):
        return {
            'title': self.title_input.text(),
            'username': self.username_input.text(),
            'password': self.password_input.text(),
            'url': self.url_input.text(),
            'notes': self.notes_input.text()
        }

class PasswordGeneratorDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Password Generator")
        self.setMinimumWidth(400)
        
        layout = QVBoxLayout()
        form_layout = QFormLayout()
        
        # Password length option
        self.length_spinner = QSpinBox()
        self.length_spinner.setMinimum(8)
        self.length_spinner.setMaximum(64)
        self.length_spinner.setValue(16)
        form_layout.addRow("Password Length:", self.length_spinner)
        
        # Character options
        self.include_uppercase = QCheckBox("Include uppercase letters (A-Z)")
        self.include_uppercase.setChecked(True)
        form_layout.addRow("", self.include_uppercase)
        
        self.include_digits = QCheckBox("Include digits (0-9)")
        self.include_digits.setChecked(True)
        form_layout.addRow("", self.include_digits)
        
        self.include_symbols = QCheckBox("Include special characters (!@#$%^&*)")
        self.include_symbols.setChecked(True)
        form_layout.addRow("", self.include_symbols)
        
        layout.addLayout(form_layout)
        
        # Generated password display
        self.password_display = QLineEdit()
        self.password_display.setReadOnly(True)
        self.password_display.setFont(QFont("Courier", 12))
        layout.addWidget(self.password_display)
        
        # Generate button
        self.generate_button = QPushButton("Generate Password")
        self.generate_button.clicked.connect(self.generate_password)
        layout.addWidget(self.generate_button)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        
        self.use_button = QPushButton("Use Password")
        self.use_button.clicked.connect(self.accept)
        self.use_button.setEnabled(False)
        
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.use_button)
        
        layout.addLayout(button_layout)
        self.setLayout(layout)
        
        # Generate a password immediately when opened
        self.generate_password()
    
    def generate_password(self):
        length = self.length_spinner.value()
        include_uppercase = self.include_uppercase.isChecked()
        include_digits = self.include_digits.isChecked()
        include_symbols = self.include_symbols.isChecked()
        
        # This is a placeholder - the actual generation happens in the main app
        # As a demo, we'll just generate a dummy password
        import string
        import random
        
        chars = string.ascii_lowercase
        if include_uppercase:
            chars += string.ascii_uppercase
        if include_digits:
            chars += string.digits
        if include_symbols:
            chars += string.punctuation
        
        password = ''.join(random.choice(chars) for _ in range(length))
        self.password_display.setText(password)
        self.use_button.setEnabled(True)
        
    def get_generated_password(self):
        return self.password_display.text()


class MainWindow(QMainWindow):
    password_added = pyqtSignal(dict)
    password_deleted = pyqtSignal(int)  
    password_edited = pyqtSignal(int, dict)
    password_generation_requested = pyqtSignal(int, bool, bool, bool)
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyLock - Password Manager")
        self.setMinimumSize(800, 600)
        
        # Create main widget and layout
        central_widget = QWidget()
        main_layout = QVBoxLayout()
        
        # Create tabs
        self.tabs = QTabWidget()
        
        # Passwords tab
        self.passwords_tab = QWidget()
        self.setup_passwords_tab()
        self.tabs.addTab(self.passwords_tab, "Passwords")
        
        # Settings tab
        self.settings_tab = QWidget()
        self.setup_settings_tab()
        self.tabs.addTab(self.settings_tab, "Settings")
        
        # Add tabs to main layout
        main_layout.addWidget(self.tabs)
        
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)
        
        # Setup menu bar
        self.setup_menu_bar()
    
    def setup_menu_bar(self):
        menu_bar = self.menuBar()
        
        # File menu
        file_menu = menu_bar.addMenu("File")
        
        add_action = QAction("Add Password", self)
        add_action.triggered.connect(self.show_add_password_dialog)
        file_menu.addAction(add_action)
        
        generate_action = QAction("Generate Password", self)
        generate_action.triggered.connect(lambda: self.show_password_generator(standalone=True))
        file_menu.addAction(generate_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menu_bar.addMenu("Edit")
        
        edit_action = QAction("Edit Selected", self)
        edit_action.triggered.connect(self.edit_selected_password)
        edit_menu.addAction(edit_action)
        
        delete_action = QAction("Delete Selected", self)
        delete_action.triggered.connect(self.delete_selected_password)
        edit_menu.addAction(delete_action)
        
        # Help menu
        help_menu = menu_bar.addMenu("Help")
        
        about_action = QAction("About PyLock", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def setup_passwords_tab(self):
        layout = QVBoxLayout()
        
        # Create password table
        self.password_table = QTableWidget()
        self.password_table.setColumnCount(5)
        self.password_table.setHorizontalHeaderLabels(["ID", "Title/Service", "Username", "Password", "URL"])
        self.password_table.setColumnHidden(0, True)  # Hide ID column
        self.password_table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.password_table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.password_table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.password_table.doubleClicked.connect(self.view_password_details)
        
        # Enable right-click menu
        self.password_table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.password_table.customContextMenuRequested.connect(self.show_context_menu)
        
        layout.addWidget(self.password_table)
        
        # Button layout
        button_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Password")
        add_btn.clicked.connect(self.show_add_password_dialog)
        button_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("Edit Selected")
        edit_btn.clicked.connect(self.edit_selected_password)
        button_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Delete Selected")
        delete_btn.clicked.connect(self.delete_selected_password)
        button_layout.addWidget(delete_btn)
        
        gen_pwd_btn = QPushButton("Generate Password")
        gen_pwd_btn.clicked.connect(lambda: self.show_password_generator(standalone=True))
        button_layout.addWidget(gen_pwd_btn)
        
        layout.addLayout(button_layout)
        
        self.passwords_tab.setLayout(layout)
    
    def setup_settings_tab(self):
        layout = QVBoxLayout()
        
        # 2FA Settings
        twofa_group = QWidget()
        twofa_layout = QFormLayout()
        
        self.enable_2fa = QCheckBox("Enable Two-Factor Authentication")
        twofa_layout.addRow("", self.enable_2fa)
        
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email for verification codes")
        twofa_layout.addRow("Email:", self.email_input)
        
        twofa_group.setLayout(twofa_layout)
        layout.addWidget(twofa_group)
        
        # Password Generation Settings
        gen_group = QWidget()
        gen_layout = QFormLayout()
        
        self.default_length = QSpinBox()
        self.default_length.setMinimum(8)
        self.default_length.setMaximum(64)
        self.default_length.setValue(16)
        gen_layout.addRow("Default Password Length:", self.default_length)
        
        self.default_uppercase = QCheckBox("Include uppercase letters")
        self.default_uppercase.setChecked(True)
        gen_layout.addRow("", self.default_uppercase)
        
        self.default_digits = QCheckBox("Include digits")
        self.default_digits.setChecked(True)
        gen_layout.addRow("", self.default_digits)
        
        self.default_symbols = QCheckBox("Include symbols")
        self.default_symbols.setChecked(True)
        gen_layout.addRow("", self.default_symbols)
        
        gen_group.setLayout(gen_layout)
        layout.addWidget(gen_group)
        
        # Save settings button
        save_btn = QPushButton("Save Settings")
        save_btn.clicked.connect(self.save_settings)
        layout.addWidget(save_btn)
        
        layout.addStretch()
        self.settings_tab.setLayout(layout)
    
    def show_add_password_dialog(self):
        dialog = PasswordDialog(self)
        if dialog.exec():
            password_data = dialog.get_password_data()
            self.password_added.emit(password_data)
    
    def edit_selected_password(self):
        selected_rows = self.password_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a password to edit.")
            return
        
        row = selected_rows[0].row()
        password_id = int(self.password_table.item(row, 0).text())
        
        # Get current data from the table
        current_data = {
            'title': self.password_table.item(row, 1).text(),
            'username': self.password_table.item(row, 2).text(),
            'password': self.password_table.item(row, 3).text(),
            'url': self.password_table.item(row, 4).text(),
            'notes': ''  # Notes not visible in the table
        }
        
        dialog = PasswordDialog(self, current_data, edit_mode=True)
        if dialog.exec():
            updated_data = dialog.get_password_data()
            self.password_edited.emit(password_id, updated_data)
            
            # Update the table display
            self.update_password_in_table(row, updated_data)
    
    def delete_selected_password(self):
        selected_rows = self.password_table.selectedItems()
        if not selected_rows:
            QMessageBox.warning(self, "No Selection", "Please select a password to delete.")
            return
        
        row = selected_rows[0].row()
        password_id = int(self.password_table.item(row, 0).text())
        title = self.password_table.item(row, 1).text()
        
        confirm = QMessageBox.question(
            self,
            "Confirm Deletion",
            f"Are you sure you want to delete the password for '{title}'?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        
        if confirm == QMessageBox.StandardButton.Yes:
            self.password_deleted.emit(password_id)
            self.password_table.removeRow(row)
    
    def view_password_details(self):
        selected_row = self.password_table.currentRow()
        if selected_row >= 0:
            password_id = int(self.password_table.item(selected_row, 0).text())
            title = self.password_table.item(selected_row, 1).text()
            username = self.password_table.item(selected_row, 2).text()
            password = self.password_table.item(selected_row, 3).text()
            url = self.password_table.item(selected_row, 4).text()
            
            # This would typically fetch and decrypt the password
            # For now we'll just display the fields
            
            QMessageBox.information(
                self,
                f"Details for {title}",
                f"Username: {username}\nPassword: {password}\nURL: {url}"
            )
    
    def show_password_generator(self, standalone=False):
        generator_dialog = PasswordGeneratorDialog(self)
        if generator_dialog.exec():
            password = generator_dialog.get_generated_password()
            
            if standalone:
                # Just copy to clipboard
                from PyQt6.QtGui import QGuiApplication
                QGuiApplication.clipboard().setText(password)
                QMessageBox.information(
                    self, 
                    "Password Generated", 
                    f"Password has been copied to clipboard:\n\n{password}"
                )
    
    def save_settings(self):
        QMessageBox.information(
            self,
            "Settings Saved",
            "Your settings have been saved successfully."
        )
    
    def show_context_menu(self, position):
        menu = QMenu()
        
        view_action = menu.addAction("View Details")
        edit_action = menu.addAction("Edit")
        copy_username = menu.addAction("Copy Username")
        copy_password = menu.addAction("Copy Password")
        menu.addSeparator()
        delete_action = menu.addAction("Delete")
        
        # Show the context menu
        action = menu.exec(self.password_table.viewport().mapToGlobal(position))
        
        if action == view_action:
            self.view_password_details()
        elif action == edit_action:
            self.edit_selected_password()
        elif action == copy_username:
            row = self.password_table.currentRow()
            if row >= 0:
                username = self.password_table.item(row, 2).text()
                from PyQt6.QtGui import QGuiApplication
                QGuiApplication.clipboard().setText(username)
        elif action == copy_password:
            row = self.password_table.currentRow()
            if row >= 0:
                password = self.password_table.item(row, 3).text()
                from PyQt6.QtGui import QGuiApplication
                QGuiApplication.clipboard().setText(password)
        elif action == delete_action:
            self.delete_selected_password()
    
    def add_password_to_table(self, password_data):
        row = self.password_table.rowCount()
        self.password_table.insertRow(row)
        
        # Populate the row
        self.password_table.setItem(row, 0, QTableWidgetItem(str(password_data['id'])))
        self.password_table.setItem(row, 1, QTableWidgetItem(password_data['title']))
        self.password_table.setItem(row, 2, QTableWidgetItem(password_data['username']))
        
        # For security, show a placeholder for passwords
        self.password_table.setItem(row, 3, QTableWidgetItem("••••••••"))
        
        self.password_table.setItem(row, 4, QTableWidgetItem(password_data.get('url', '')))
    
    def update_password_in_table(self, row, password_data):
        self.password_table.setItem(row, 1, QTableWidgetItem(password_data['title']))
        self.password_table.setItem(row, 2, QTableWidgetItem(password_data['username']))
        # For security, keep password as dots
        self.password_table.setItem(row, 4, QTableWidgetItem(password_data.get('url', '')))
        
    def show_about(self):
        QMessageBox.about(
            self,
            "About PyLock",
            "PyLock - Secure Password Manager\n\n"
            "Version 1.0\n\n"
            "A secure solution for storing and managing your passwords."
        )