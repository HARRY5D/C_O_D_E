'''
from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
from datetime import datetime

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            df = pd.read_excel(file)
            # Assuming the date is in a column named 'Policy End Date'
            dates = df['Policy End Date'].tolist()
            # Convert dates to string for display
            dates = [date.strftime('%Y-%m-%d') if isinstance(date, datetime) else str(date) for date in dates]
            return render_template('confirm_dates.html', dates=dates)
    return render_template('upload.html')

@app.route('/confirm', methods=['POST'])
def confirm_dates():
    # Get the confirmed dates from the form
    confirmed_dates = request.form.getlist('dates')
    # Here you would save the dates and set up notifications
    return "Dates confirmed: " + ", ".join(confirmed_dates)

if __name__ == '__main__':
    app.run(debug=True)

'''
'''
# app.py
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '23dce080@charusat.edu.in'
app.config['MAIL_PASSWORD'] = 'sender'
mail = Mail(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # Ensure this matches the login route

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    end_date = db.Column(db.Date, nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def send_email(subject, body, to_email):
    msg = Message(subject, sender='23dce080@charusat.edu.in', recipients=[to_email])
    msg.body = body
    mail.send(msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('upload_file'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            send_email("Password Reset Request", f"Your password is: {user.password}", user.email)
            flash('Password reset email sent!', 'info')
        else:
            flash('Email not found!', 'danger')
    return render_template('forgot_password.html')

@app.route('/', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        # Check if a file is uploaded
        file = request.files.get('file')
        if file:
            df = pd.read_excel(file)
            dates = df['Policy End Date'].tolist()
            dates = [date.strftime('%Y-%m-%d') if isinstance(date, datetime) else str(date) for date in dates]
            return render_template('confirm_dates.html', dates=dates)
        
        # Handle manual entry
        policy_name = request.form.get('policy_name')
        policy_end_date = request.form.get('policy_end_date')
        notify_before = int(request.form.get('notify_before'))
        
        # Convert policy_end_date to a date object
        end_date = datetime.strptime(policy_end_date, '%Y-%m-%d').date()
        
        # Calculate notification date
        notification_date = end_date - timedelta(days=notify_before)
        
        # Save policy details to the database
        policy = Policy(user_id=current_user.id, end_date=end_date)
        db.session.add(policy)
        db.session.commit()
        
        # Schedule notification (this is a placeholder, implement scheduling logic)
        send_email("Policy Reminder", f"Your policy '{policy_name}' ends on {end_date}.", current_user.email)
        
        return "Policy details submitted and notification scheduled!"
    return render_template('upload.html')

@app.route('/confirm', methods=['POST'])
@login_required
def confirm_dates():
    confirmed_dates = request.form.getlist('dates')
    for date_str in confirmed_dates:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        policy = Policy(user_id=current_user.id, end_date=date)
        db.session.add(policy)
    db.session.commit()
    for date in confirmed_dates:
        send_email("Policy Reminder", f"Your policy ends on {date}.", current_user.email)
    return "Dates confirmed and emails sent!"

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
    '''
# app.py
'''
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
import pandas as pd
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from typing import Optional

app = Flask(__name__)
app.config['SECRET_KEY'] = 'key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = '23dce080@charusat.edu.in'
app.config['MAIL_PASSWORD'] = 'sender'
mail = Mail(app)
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view: Optional[str] = 'login'

class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    policy_name = db.Column(db.String(100), nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    notify_before = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    notification_date = db.Column(db.DateTime, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, policy_name: str, end_date: datetime, notify_before: int, 
                 user_id: int, notification_date: datetime):
        self.policy_name = policy_name
        self.end_date = end_date
        self.notify_before = notify_before
        self.user_id = user_id
        self.notification_date = notification_date

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    policies = db.relationship('Policy', backref='user', lazy=True)

    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def send_email(subject, body, to_email):
    try:
        msg = Message(subject, sender='23dce080@charusat.edu.in', recipients=[to_email])
        msg.body = body
        mail.send(msg)
    except Exception as e:
        print(f"Failed to send email: {e}")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            hashed_password = generate_password_hash(password, method='sha256')
            user = User(email=email, password=hashed_password)
            db.session.add(user)
            db.session.commit()
            flash('Account created successfully!', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if email and password:
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for('upload_file'))
            else:
                flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        if email:
            user = User.query.filter_by(email=email).first()
            if user:
                send_email("Password Reset Request", f"Your password is: {user.password}", user.email)
                flash('Password reset email sent!', 'info')
            else:
                flash('Email not found!', 'danger')
    return render_template('forgot_password.html')

@app.route('/', methods=['GET', 'POST'])
@login_required
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            try:
                df = pd.read_excel(file)
                dates = df['Policy End Date'].tolist()
                dates = [date.strftime('%Y-%m-%d') if isinstance(date, datetime) else str(date) for date in dates]
                return render_template('confirm_dates.html', dates=dates)
            except Exception as e:
                flash(f'Error processing file: {str(e)}', 'danger')
                return redirect(url_for('upload_file'))
        
        try:
            policy_name: Optional[str] = request.form.get('policy_name')
            policy_end_date: Optional[str] = request.form.get('policy_end_date')
            notify_before_str: Optional[str] = request.form.get('notify_before')

            if not all([policy_name, policy_end_date, notify_before_str]):
                flash('Please fill in all fields', 'danger')
                return redirect(url_for('upload_file'))

            try:
                end_date = datetime.strptime(str(policy_end_date), '%Y-%m-%d')
            except ValueError:
                flash('Invalid date format. Please use YYYY-MM-DD', 'danger')
                return redirect(url_for('upload_file'))

            notify_before = int(str(notify_before_str))
            notification_date = end_date - timedelta(days=notify_before)

            new_policy = Policy(
                policy_name=str(policy_name),
                end_date=end_date,
                notify_before=notify_before,
                user_id=current_user.id,
                notification_date=notification_date
            )

            db.session.add(new_policy)
            db.session.commit()

            send_email(
                subject="Policy Reminder", 
                body=f"Your policy '{policy_name}' ends on {end_date.strftime('%Y-%m-%d')}.", 
                to_email=current_user.email
            )

            flash('Policy added successfully!', 'success')
            return redirect(url_for('upload_file'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error saving policy: {str(e)}', 'danger')
            return redirect(url_for('upload_file'))

    return render_template('upload.html')

@app.route('/confirm', methods=['POST'])
@login_required
def confirm_dates():
    confirmed_dates = request.form.getlist('dates')
    for date_str in confirmed_dates:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            policy = Policy(
                policy_name="Imported Policy",
                end_date=date,
                notify_before=1,  # Default notification period
                user_id=current_user.id,
                notification_date=date - timedelta(days=1)
            )
            db.session.add(policy)
        except ValueError:
            flash(f'Invalid date format: {date_str}', 'danger')
            return redirect(url_for('upload_file'))
    
    db.session.commit()
    flash('Dates confirmed and notifications scheduled!', 'success')
    return redirect(url_for('upload_file'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)


    '''

'''
from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import pandas as pd
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['MAIL_USERNAME'] = 'harnishdpatel@gmail.com'  # Your Gmail address
app.config['MAIL_PASSWORD'] = 'Harnish@123'  # App password from step 2

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    policies = db.relationship('Policy', backref='user', lazy=True)

class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    policy_name = db.Column(db.String(100), nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    notify_before = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])

def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            try:
                df = pd.read_excel(file)
                dates = df['Policy End Date'].tolist()
                dates = [date.strftime('%Y-%m-%d') if isinstance(date, datetime) else str(date) for date in dates]
                return render_template('confirm_dates.html', dates=dates)
            except Exception as e:
                flash(f'Error processing file: {str(e)}', 'danger')
                return redirect(url_for('upload_file'))
        
        try:
            policy_name = request.form.get('policy_name')
            policy_end_date = request.form.get('policy_end_date')
            notify_before_str = request.form.get('notify_before')

            if not all([policy_name, policy_end_date, notify_before_str]):
                flash('Please fill in all fields', 'danger')
                return redirect(url_for('upload_file'))

            end_date = datetime.strptime(policy_end_date, '%Y-%m-%d')
            notify_before = int(notify_before_str)

            new_policy = Policy(
                policy_name=policy_name,
                end_date=end_date,
                notify_before=notify_before,
                user_id=1  # Default user ID for testing
            )

            db.session.add(new_policy)
            db.session.commit()
            flash('Policy added successfully!', 'success')
            return redirect(url_for('upload_file'))

        except Exception as e:
            db.session.rollback()
            flash(f'Error saving policy: {str(e)}', 'danger')
            return redirect(url_for('upload_file'))

    return render_template('upload.html')

@app.route('/confirm', methods=['POST'])
def confirm_dates():
    confirmed_dates = request.form.getlist('dates')
    for date_str in confirmed_dates:
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            policy = Policy(
                policy_name="Imported Policy",
                end_date=date,
                notify_before=1,
                user_id=1  # Default user ID for testing
            )
            db.session.add(policy)
        except ValueError:
            flash(f'Invalid date format: {date_str}', 'danger')
            return redirect(url_for('upload_file'))
        
        
    
    db.session.commit()
    flash('Dates confirmed and saved!', 'success')
    return redirect(url_for('upload_file'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

#     '''
from flask import Flask, request, jsonify, render_template
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
import logging
import os

app = Flask(__name__)
CORS(app)

# Configuration
app.config.update(
    SECRET_KEY='your-secret-key',
    SQLALCHEMY_DATABASE_URI='sqlite:///policy_reminder.db',
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_TLS=True,
    MAIL_USERNAME='harnishdpatel@gmail.com',
    MAIL_PASSWORD='zmzn qlyx wafm tdte'
)

# Initialize extensions
db = SQLAlchemy(app)
mail = Mail(app)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    name = db.Column(db.String(100))
    reminders = db.relationship('Reminder', backref='user', lazy=True)

    def __init__(self, email, password, name=None):
        self.email = email
        self.password = password
        self.name = name

class Reminder(db.Model):
    __tablename__ = 'reminders'
    id = db.Column(db.Integer, primary_key=True)
    policy_name = db.Column(db.String(100), nullable=False)
    expiry_date = db.Column(db.DateTime, nullable=False)
    reminder_days = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, policy_name, expiry_date, reminder_days, user_id):
        self.policy_name = policy_name
        self.expiry_date = expiry_date
        self.reminder_days = reminder_days
        self.user_id = user_id

@app.route('/')
def index():
    return render_template('policy_manager.html')

@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email')
        password = data.get('password')
        name = data.get('name')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        if User.query.filter_by(email=email).first():
            return jsonify({'error': 'Email already registered'}), 400
        
        new_user = User(email=email, password=password, name=name)
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({
            'message': 'Registration successful',
            'user': {'email': email, 'name': name}
        }), 201
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({'error': 'Registration failed'}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        user = User.query.filter_by(email=email, password=password).first()
        
        if user:
            return jsonify({
                'message': 'Login successful',
                'user': {'email': user.email, 'name': user.name}
            }), 200
        return jsonify({'error': 'Invalid credentials'}), 401
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({'error': 'Login failed'}), 500

@app.route('/reminder', methods=['POST'])
def add_reminder():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        user_email = data.get('userEmail')
        policy_name = data.get('policyName')
        expiry_date = data.get('expiryDate')
        reminder_days = data.get('reminderDays')
        
        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        new_reminder = Reminder(
            policy_name=policy_name,
            expiry_date=datetime.strptime(expiry_date, '%Y-%m-%d'),
            reminder_days=int(reminder_days),
            user_id=user.id
        )
        
        db.session.add(new_reminder)
        db.session.commit()
        
        # Send email notification
        send_reminder_email(user.email, policy_name, expiry_date, reminder_days)
        
        return jsonify({'message': 'Reminder added successfully'}), 201
    except Exception as e:
        logger.error(f"Error adding reminder: {str(e)}")
        return jsonify({'error': 'Failed to add reminder'}), 500

@app.route('/reminders/<email>', methods=['GET'])
def get_reminders(email):
    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': 'User not found'}), 404
        
        reminders = [{
            'id': r.id,
            'policyName': r.policy_name,
            'expiryDate': r.expiry_date.strftime('%Y-%m-%d'),
            'reminderDays': r.reminder_days
        } for r in user.reminders]
        
        return jsonify({'reminders': reminders}), 200
    except Exception as e:
        logger.error(f"Error getting reminders: {str(e)}")
        return jsonify({'error': 'Failed to get reminders'}), 500

@app.route('/reminder/<int:id>', methods=['DELETE'])
def delete_reminder(id):
    try:
        reminder = Reminder.query.get(id)
        if not reminder:
            return jsonify({'error': 'Reminder not found'}), 404
        
        db.session.delete(reminder)
        db.session.commit()
        return jsonify({'message': 'Reminder deleted successfully'}), 200
    except Exception as e:
        logger.error(f"Error deleting reminder: {str(e)}")
        return jsonify({'error': 'Failed to delete reminder'}), 500

def send_reminder_email(to_email, policy_name, expiry_date, days_remaining):
    try:
        msg = Message('Policy Expiry Reminder',
                     sender=app.config['MAIL_USERNAME'],
                     recipients=[to_email])
        
        msg.body = f"""
        Dear User,

        Your policy "{policy_name}" will expire on {expiry_date}.
        This is a reminder that you have {days_remaining} days remaining.

        Best regards,
        Policy Reminder System
        """
        
        mail.send(msg)
        logger.info(f"Reminder email sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send reminder email: {str(e)}")
        return False

@app.route('/reset-password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        if not data or not data.get('email'):
            return jsonify({'error': 'Email is required'}), 400
        
        user = User.query.filter_by(email=data['email']).first()
        if not user:
            return jsonify({'error': 'Email not found'}), 404
        
        temp_password = os.urandom(4).hex()
        user.password = temp_password
        db.session.commit()
        
        msg = Message('Password Reset',
                     sender=app.config['MAIL_USERNAME'],
                     recipients=[user.email])
        
        msg.body = f"""
        Your temporary password is: {temp_password}
        Please login and change your password immediately.
        """
        
        mail.send(msg)
        return jsonify({'message': 'Password reset email sent'}), 200
    except Exception as e:
        logger.error(f"Password reset error: {str(e)}")
        return jsonify({'error': 'Failed to reset password'}), 500

# At the bottom of app.py, change the run line to:
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5502, debug=True)
