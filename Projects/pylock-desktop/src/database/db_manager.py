import sqlite3
import os

class DatabaseManager:
    def __init__(self, db_path=None):
        if db_path is None:
            # Default to user's app data directory
            app_data_dir = os.path.join(os.path.expanduser('~'), 'PyLock')
            os.makedirs(app_data_dir, exist_ok=True)
            db_path = os.path.join(app_data_dir, 'passwords.db')
            
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()

        # Create users table with verification_code, special_sentence, and first_login columns
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                username TEXT UNIQUE,
                password_hash TEXT,
                salt TEXT,
                email TEXT,
                phone TEXT,
                verified INTEGER DEFAULT 0,
                verification_code TEXT,
                special_sentence TEXT,
                first_login INTEGER DEFAULT 1
            )
            """
        )

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
            cursor.execute("ALTER TABLE users ADD COLUMN first_login INTEGER DEFAULT 1")
        except sqlite3.OperationalError:
            # Column already exists, ignore
            pass

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                service TEXT,
                username TEXT,
                password TEXT,
                iv TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE CASCADE
            )
            """
        )
        self.conn.commit()

    def execute_query(self, query, params=()):
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        self.conn.commit()
        return cursor
    
    def close(self):
        """Close the database connection"""
        if self.conn:
            self.conn.close()
    
    def __del__(self):
        """Destructor to ensure database connection is closed"""
        self.close()