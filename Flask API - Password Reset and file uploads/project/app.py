from enum import unique
from flask import Flask, json, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from random import randint
from datetime import datetime, timedelta
import smtplib
from email.message import EmailMessage


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique = True, nullable = False)
    password = db.Column(db.String(30), nullable = False)
    reset_otp = db.Column(db.String(6), nullable = True)
    otp_timestamp = db.Column(db.DateTime, nullable = True)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def home():
    return 'Hola'

def send_email(subject, user, message):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'captain.smartass1@gmail.com'
    msg['To'] = user.email
    msg.set_content(message)
    with smtplib.SMTP_SSL('smtp.gmail.com',465) as smtp:
        smtp.login('captain.smartass1@gmail.com','deadpool1@')
        smtp.send_message(msg)

@app.route('/register', methods = ['POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        user = User(email = data['email'], password = data['password'])
        db.session.add(user)
        db.session.commit()
        return  jsonify({'message': 'User reigstered'})

@app.route('/users')
def get_users():
    return jsonify({"users": [{"email": data.email, "password": data.password} for data in User.query.all()]})

@app.route('/forgot-password', methods = ['POST'])
def forgot_password():
    if request.method == "POST":
        data = request.get_json()
        user = User.query.filter_by(email = data['email'])[0]
        otp = randint(100000, 999999)
        user.reset_otp = otp
        user.otp_timestamp = datetime.now()
        db.session.commit()
        send_email('Password Reset', user, f'You have raised a request to reset your password. Make use of this otp {otp}. This OTP is valid for 3 hours. Visit http://localhost:5000/reset-password to set your new password.')
        return jsonify({'messsage': 'OTP and password reset link has been sent to your email. This OTP is valid for 3 hours.'})

@app.route('/reset-password', methods = ['POST'])
def reset_password():
    data = request.get_json()
    user = User.query.filter_by(email = data['email'])[0]
    if user.reset_otp == data['otp'] and (datetime.now() - user.otp_timestamp) < timedelta(hours = 3):
        user.password = data['password']
        db.session.commit()
        return jsonify({'message': 'Password reset successfully'})
    return jsonify({'message': 'Invalid OTP / OTP Expired'})

app.run(debug = True)