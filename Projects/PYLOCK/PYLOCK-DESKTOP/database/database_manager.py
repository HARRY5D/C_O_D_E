import sqlite3
from typing import List, Dict, Optional

class DatabaseManager:
    def __init__(self, db_file: str = "passwords.db"):
        self.db_file = db_file
        self.setup_database()
    
    def setup_database(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_data (
                    id TEXT PRIMARY KEY,
                    master_hash TEXT NOT NULL,
                    salt BLOB NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    username TEXT,
                    encrypted_password BLOB NOT NULL,
                    url TEXT,
                    notes TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def save_user(self, user_id: str, master_hash: str, salt: bytes):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR REPLACE INTO user_data (id, master_hash, salt) VALUES (?, ?, ?)",
                (user_id, master_hash, salt)
            )
            conn.commit()
    
    def get_user(self, user_id: str) -> Optional[Dict]:
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT master_hash, salt FROM user_data WHERE id = ?",
                (user_id,)
            )
            result = cursor.fetchone()
            if result:
                return {"master_hash": result[0], "salt": result[1]}
            return None
    
    def save_password(self, title: str, username: str, encrypted_password: bytes,
                     url: str = "", notes: str = "") -> int:
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO passwords 
                   (title, username, encrypted_password, url, notes)
                   VALUES (?, ?, ?, ?, ?)""",
                (title, username, encrypted_password, url, notes)
            )
            conn.commit()
            return cursor.lastrowid
    
    def get_all_passwords(self) -> List[Dict]:
        with sqlite3.connect(self.db_file) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM passwords ORDER BY title")
            return [dict(row) for row in cursor.fetchall()]
    
    def update_password(self, password_id: int, title: str, username: str,
                       encrypted_password: bytes, url: str, notes: str):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute(
                """UPDATE passwords 
                   SET title=?, username=?, encrypted_password=?, url=?, notes=?
                   WHERE id=?""",
                (title, username, encrypted_password, url, notes, password_id)
            )
            conn.commit()
    
    def delete_password(self, password_id: int):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM passwords WHERE id=?", (password_id,))
            conn.commit()