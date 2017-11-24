import os
import re
from flask import Flask
from flask import request
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from wtforms import Form, StringField, validators
from flask_bcrypt import Bcrypt
import jwt

app = Flask(__name__)
bcrypt = Bcrypt(app)

SECRET_KEY = os.getenv('SECRET_KEY')
JWT_ALGORITHM = 'HS256'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/api-auth-flask-dev'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_digest = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_digest = str(bcrypt.generate_password_hash(password), 'utf-8')

    def verify_password(self, password):
        return password and bcrypt.check_password_hash(self.password_digest, password)

    def public_attributes(self):
        return {'name': self.name, 'email': self.email}

    def __repr__(self):
        return '<User %r>' % self.email

class UserForm(Form):
    email = StringField('Email', [validators.Required(), validators.Length(min=3, max=80)])
    password = StringField('Password', [validators.Required(), validators.Length(min=3, max=80)])
    name = StringField('Name', [validators.Optional(), validators.Length(min=3, max=80)])

@app.route('/register', methods=['POST'])
def register():
    attributes = request.get_json().get('user', {})
    form = UserForm(**attributes)
    if form.validate():
        user = User(**attributes)
        db.session.add(user)
        db.session.commit()
        return (jsonify({'user': user.public_attributes()}), 201)
    else:
        return (jsonify({'errors': form.errors}), 422)

@app.route('/login', methods=['POST'])
def login():
    params = request.get_json()
    user = User.query.filter_by(email=params['email']).first()
    success = user and user.verify_password(params['password'])
    if success:
        token = str(jwt.encode({'user_id': user.id}, SECRET_KEY, algorithm=JWT_ALGORITHM), 'utf-8')
        return jsonify({'token': token})
    else:
        return (jsonify({'error': 'invalid credentials'}), 401)

@app.route('/me')
def me():
    header_match = re.search('^Bearer (.+)$', request.headers.get('Authorization', ''))
    token = header_match and header_match.group(1)
    if token:
        claims = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
        user = User.query.get(claims['user_id'])
        return jsonify({'user': user.public_attributes()})
    else:
        return (jsonify({'error': 'unauthorized'}), 401)
