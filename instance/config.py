class Config:
    SECRET_KEY = 'your-secret-key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'harnishdpatel@gmail.com'
    MAIL_PASSWORD = 'Harnish123'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///policy_reminder.db'
    SERVER_NAME = 'localhost:5500'

class ProductionConfig(Config):
    DEBUG = False
    # For production, use PostgreSQL
    SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/dbname'
    SERVER_NAME = 'yourdomain.com'  # Replace with your domain