from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from cryptography.fernet import Fernet
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pylock.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Password(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    website = db.Column(db.String(150), nullable=False)

def generate_key():
    return Fernet.generate_key()

def encrypt_password(key, password):
    f = Fernet(key)
    return f.encrypt(password.encode()).decode()

def decrypt_password(key, encrypted_password):
    f = Fernet(key)
    return f.decrypt(encrypted_password.encode()).decode()

key = generate_key()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_password', methods=['POST'])
def add_password():
    data = request.get_json()
    username = data['username']
    password = data['password']
    website = data['website']
    encrypted_password = encrypt_password(key, password)
    new_password = Password(username=username, password=encrypted_password, website=website)
    db.session.add(new_password)
    db.session.commit()
    return jsonify({'message': 'Password added successfully!'})

@app.route('/view_passwords', methods=['GET'])
def view_passwords():
    passwords = Password.query.all()
    output = []
    for password in passwords:
        decrypted_password = decrypt_password(key, password.password)
        password_data = {'username': password.username, 'password': decrypted_password, 'website': password.website}
        output.append(password_data)
    return jsonify({'passwords': output})

@app.route('/edit_password/<int:id>', methods=['PUT'])
def edit_password(id):
    data = request.get_json()
    password = Password.query.get(id)
    if not password:
        return jsonify({'message': 'Password not found'}), 404
    password.username = data['username']
    password.password = encrypt_password(key, data['password'])
    password.website = data['website']
    db.session.commit()
    return jsonify({'message': 'Password updated successfully!'})

@app.route('/delete_password/<int:id>', methods=['DELETE'])
def delete_password(id):
    password = Password.query.get(id)
    if not password:
        return jsonify({'message': 'Password not found'}), 404
    db.session.delete(password)
    db.session.commit()
    return jsonify({'message': 'Password deleted successfully!'})

@app.route('/search_passwords', methods=['GET'])
def search_passwords():
    query = request.args.get('query')
    passwords = Password.query.filter(Password.website.contains(query)).all()
    output = []
    for password in passwords:
        decrypted_password = decrypt_password(key, password.password)
        password_data = {'username': password.username, 'password': decrypted_password, 'website': password.website}
        output.append(password_data)
    return jsonify({'passwords': output})

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
