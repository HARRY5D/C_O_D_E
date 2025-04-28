import sqlite3
import json

class DatabaseManager:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Create users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                key_hash TEXT,
                salt TEXT,
                email TEXT,
                phone TEXT,
                special_sentence TEXT,
                verification_code TEXT,
                verified INTEGER DEFAULT 0,
                first_login INTEGER DEFAULT 1
            )
        ''')
        
        # Create passwords table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                title TEXT,
                username TEXT,
                encrypted_password TEXT,
                url TEXT,
                notes TEXT,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Make sure all columns exist (for older databases)
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN verification_code TEXT")
        except sqlite3.OperationalError:
            # Column already exists, ignore
            pass

        try:
            cursor.execute("ALTER TABLE users ADD COLUMN special_sentence TEXT")
        except sqlite3.OperationalError:
            # Column already exists, ignore
            pass
            
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")
        except sqlite3.OperationalError:
            # Column already exists, ignore
            pass
            
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT")
        except sqlite3.OperationalError:
            # Column already exists, ignore
            pass
            
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN verified INTEGER DEFAULT 0")
        except sqlite3.OperationalError:
            # Column already exists, ignore
            pass
            
        try:
            cursor.execute("ALTER TABLE users ADD COLUMN first_login INTEGER DEFAULT 1")
        except sqlite3.OperationalError:
            # Column already exists, ignore
            pass
            
        self.conn.commit()
        
    def save_user(self, user_id, key_hash, salt, special_sentence, email=None, phone=None):
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            INSERT OR REPLACE INTO users (id, key_hash, salt, special_sentence, email, phone)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (user_id, key_hash, salt, special_sentence, email, phone)
        )
        self.conn.commit()
        
    def update_user_email(self, user_id, email):
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            UPDATE users SET email = ? WHERE id = ?
            ''',
            (email, user_id)
        )
        self.conn.commit()
        
    def update_user_phone(self, user_id, phone):
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            UPDATE users SET phone = ? WHERE id = ?
            ''',
            (phone, user_id)
        )
        self.conn.commit()
        
    def save_verification_code(self, user_id, code):
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            UPDATE users SET verification_code = ? WHERE id = ?
            ''',
            (code, user_id)
        )
        self.conn.commit()
        
    def verify_code(self, user_id, code):
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            SELECT verification_code FROM users WHERE id = ?
            ''',
            (user_id,)
        )
        result = cursor.fetchone()
        if result and result[0] == code:
            cursor.execute(
                '''
                UPDATE users SET verified = 1 WHERE id = ?
                ''',
                (user_id,)
            )
            self.conn.commit()
            return True
        return False
        
    def get_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM users WHERE id = ?', (user_id,))
        user = cursor.fetchone()
        
        if user:
            return {
                'id': user[0],
                'key_hash': user[1],
                'salt': user[2],
                'email': user[3],
                'phone': user[4],
                'special_sentence': user[5],
                'verification_code': user[6],
                'verified': user[7],
                'first_login': user[8]
            }
        return None
        
    def get_all_passwords(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            SELECT id, title, username, encrypted_password, url, notes
            FROM passwords
            WHERE user_id = ?
            ''',
            (user_id,)
        )
        
        passwords = []
        for row in cursor.fetchall():
            passwords.append({
                'id': row[0],
                'title': row[1],
                'username': row[2],
                'encrypted_password': row[3],
                'url': row[4],
                'notes': row[5]
            })
        
        return passwords
        
    def save_password(self, user_id, title, username, encrypted_password, url="", notes=""):
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            INSERT INTO passwords (user_id, title, username, encrypted_password, url, notes)
            VALUES (?, ?, ?, ?, ?, ?)
            ''',
            (user_id, title, username, encrypted_password, url, notes)
        )
        self.conn.commit()
        return cursor.lastrowid
        
    def update_password(self, password_id, title, username, encrypted_password, url="", notes=""):
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            UPDATE passwords
            SET title = ?, username = ?, encrypted_password = ?, url = ?, notes = ?
            WHERE id = ?
            ''',
            (title, username, encrypted_password, url, notes, password_id)
        )
        self.conn.commit()
        
    def delete_password(self, password_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM passwords WHERE id = ?', (password_id,))
        self.conn.commit()
        
    def verify_special_sentence(self, user_id, special_sentence):
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            SELECT special_sentence FROM users WHERE id = ?
            ''',
            (user_id,)
        )
        result = cursor.fetchone()
        if result and result[0] == special_sentence:
            return True
        return False

    def set_first_login_false(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute(
            '''
            UPDATE users SET first_login = 0 WHERE id = ?
            ''',
            (user_id,)
        )
        self.conn.commit()
        
    def close(self):
        self.conn.close()