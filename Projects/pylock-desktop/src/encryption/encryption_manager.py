import os
import secrets
import string
import base64
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes

backend = default_backend()

class EncryptionManager:
    @staticmethod
    def encrypt_password(password, master_key):
        """Encrypt a password using AES-CFB with the master key"""
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(master_key), modes.CFB(iv), backend=backend)
        encryptor = cipher.encryptor()
        ct = encryptor.update(password.encode()) + encryptor.finalize()
        return base64.urlsafe_b64encode(ct).decode(), iv.hex()

    @staticmethod
    def decrypt_password(encrypted_password, iv, master_key):
        """Decrypt a password using AES-CFB with the master key"""
        iv = bytes.fromhex(iv)
        ct = base64.urlsafe_b64decode(encrypted_password)
        cipher = Cipher(algorithms.AES(master_key), modes.CFB(iv), backend=backend)
        decryptor = cipher.decryptor()
        return (decryptor.update(ct) + decryptor.finalize()).decode()


class AuthManager:
    @staticmethod
    def hash_password(password, salt=None):
        """Hash a password using PBKDF2 with SHA-256"""
        salt = salt or os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
            backend=backend,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key.decode(), salt.hex()

    @staticmethod
    def generate_verification_code():
        """Generate a 6-digit verification code"""
        return "".join(secrets.choice(string.digits) for _ in range(6))

    @staticmethod
    def send_verification_email(receiver_email, code, sender_email, sender_password):
        """Send a verification code to the user's email"""
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        subject = "Your Password Manager Verification Code"
        body = f"""
        Your verification code is: {code}
        
        Please enter this code to verify your account.
        If you did not request this code, please ignore this email.
        """

        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "plain"))

        try:
            print(f"Attempting to send email to {receiver_email}")
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.ehlo()  # Identify to SMTP server
            server.starttls()  # Secure connection
            print("Logging into SMTP server...")
            server.login(sender_email, sender_password)
            print("Sending email...")
            server.send_message(msg)
            server.quit()
            print("Email sent successfully")
            return True
        except Exception as e:
            print(f"Email failed to send: {e}")
            return False

    @staticmethod
    def generate_special_sentence():
        """Generate a special sentence for account recovery"""
        word_lists = [
            ["apple", "banana", "cherry", "date", "blueberry", "fig", "grape", "honeydew", 
             "kiwi", "lemon", "mango", "orange", "papaya", "peach", "plum", "raspberry"],
            ["elephant", "tiger", "dolphin", "eagle", "penguin", "koala", "panda", "zebra",
             "kangaroo", "wolf", "jaguar", "seahorse", "lizard", "turtle", "raccoon", "falcon"],
            ["red", "green", "blue", "yellow", "purple", "orange", "teal", "violet",
             "indigo", "crimson", "azure", "emerald", "golden", "silver", "bronze", "coral"],
            ["sunny", "rainy", "cloudy", "snowy", "windy", "stormy", "foggy", "hazy",
             "humid", "chilly", "frosty", "breezy", "icy", "misty", "dry", "warm"]
        ]
        special_words = [secrets.choice(category) for category in word_lists]
        special_words += [secrets.choice(secrets.choice(word_lists)) for _ in range(2)]
        secrets.SystemRandom().shuffle(special_words)
        return " ".join(special_words)