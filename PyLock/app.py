from flask import Flask, request, jsonify, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_mail import Mail, Message
from cryptography.fernet import Fernet
import os
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pylock.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your.email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
mail = Mail(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    website = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class Policy(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    end_date = db.Column(db.Date, nullable=False)

def generate_key():
    return Fernet.generate_key()

def encrypt_password(key, password):
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()

def decrypt_password(key, encrypted_password):
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode()).decode()

key = generate_key()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def send_email(subject, body, to_email):
    msg = Message(subject, sender='your.email@gmail.com', recipients=[to_email])
    msg.body = body
    mail.send(msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
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
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('index'))
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
            temp_password = os.urandom(4).hex()
            user.password = generate_password_hash(temp_password, method='sha256')
            db.session.commit()
            send_email("Password Reset Request", f"Your temporary password is: {temp_password}", user.email)
            flash('Password reset email sent!', 'info')
        else:
            flash('Email not found!', 'danger')
    return render_template('forgot_password.html')

@app.route('/')
@login_required
def index():
    return render_template('index.html')

@app.route('/add_password', methods=['POST'])
@login_required
def add_password():
    data = request.get_json()
    username = data['username']
    password = data['password']
    website = data['website']
    encrypted_password = encrypt_password(key, password)
    new_password = Password(username=username, password=encrypted_password, website=website, user_id=current_user.id)
    db.session.add(new_password)
    db.session.commit()
    return jsonify({'message': 'Password added successfully!'})

@app.route('/view_passwords', methods=['GET'])
@login_required
def view_passwords():
    passwords = Password.query.filter_by(user_id=current_user.id).all()
    output = []
    for password in passwords:
        decrypted_password = decrypt_password(key, password.password)
        password_data = {'username': password.username, 'password': decrypted_password, 'website': password.website}
        output.append(password_data)
    return jsonify({'passwords': output})

@app.route('/edit_password/<int:id>', methods=['PUT'])
@login_required
def edit_password(id):
    data = request.get_json()
    password = Password.query.get(id)
    if not password or password.user_id != current_user.id:
        return jsonify({'message': 'Password not found'}), 404
    password.username = data['username']
    password.password = encrypt_password(key, data['password'])
    password.website = data['website']
    db.session.commit()
    return jsonify({'message': 'Password updated successfully!'})

@app.route('/delete_password/<int:id>', methods=['DELETE'])
@login_required
def delete_password(id):
    password = Password.query.get(id)
    if not password or password.user_id != current_user.id:
        return jsonify({'message': 'Password not found'}), 404
    db.session.delete(password)
    db.session.commit()
    return jsonify({'message': 'Password deleted successfully!'})

@app.route('/search_passwords', methods=['GET'])
@login_required
def search_passwords():
    query = request.args.get('query')
    passwords = Password.query.filter(Password.website.contains(query), Password.user_id == current_user.id).all()
    output = []
    for password in passwords:
        decrypted_password = decrypt_password(key, password.password)
        password_data = {'username': password.username, 'password': decrypted_password, 'website': password.website}
        output.append(password_data)
    return jsonify({'passwords': output})

@app.route('/upload_file', methods=['GET', 'POST'])
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
            policy_name = request.form.get('policy_name')
            policy_end_date = request.form.get('policy_end_date')
            notify_before_str = request.form.get('notify_before')

            if not all([policy_name, policy_end_date, notify_before_str]):
                flash('Please fill in all fields', 'danger')
                return redirect(url_for('upload_file'))

            end_date = datetime.strptime(policy_end_date, '%Y-%m-%d')
            notify_before = int(notify_before_str)
            notification_date = end_date - timedelta(days=notify_before)

            new_policy = Policy(
                policy_name=policy_name,
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
