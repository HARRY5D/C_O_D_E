from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class Encryptor:
    def __init__(self):
        self.salt = os.urandom(16)
        
    def generate_key(self, master_password: str) -> bytes:
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.b64encode(kdf.derive(master_password.encode()))
        return key
        
    def encrypt_data(self, data: str, key: bytes) -> bytes:
        f = Fernet(key)
        return f.encrypt(data.encode())
        
    def decrypt_data(self, encrypted_data: bytes, key: bytes) -> str:
        f = Fernet(key)
        return f.decrypt(encrypted_data).decode()
        
    def get_salt(self) -> bytes:
        return self.salt
        
    def set_salt(self, salt: bytes):
        self.salt = salt