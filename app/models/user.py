from app import db
from sqlalchemy.orm import relationship
from datetime import datetime
from flask_bcrypt import Bcrypt
from werkzeug.security import generate_password_hash, check_password_hash

bcrypt = Bcrypt()
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
#     first_name = db.Column(db.String(100), nullable=False)
#     last_name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     password = db.Column(db.String(255), nullable=False) 
#     User_Role = db.Column(db.String(50), nullable=False)
    
#     accounts = db.relationship('Account', backref='user', lazy=True)

#     print("Test 3 User Model ... ")
#     def __init__(self, User_Role, first_name, last_name, email, password):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.email = email
#         # self.password = password
#         self.password = bcrypt.generate_password_hash(password).decode('utf-8')
#         self.User_Role = User_Role

#         print("Registered tables:", db.Model.metadata.tables.keys())

#     def __repr__(self):
#         return f"User('{self.User_Role}', '{self.first_name}', '{self.last_name}', '{self.email}')"

#     def __str__(self):
#         return f"User: {self.User_Role} ({self.first_name} {self.last_name})"



# -------------------------
# class User(db.Model):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
#     first_name = db.Column(db.String(100), nullable=False)
#     last_name = db.Column(db.String(100), nullable=False)
#     email = db.Column(db.String(100), nullable=False)
#     password = db.Column(db.String(255), nullable=False) 
#     User_Role = db.Column(db.String(50), nullable=False)
    
#     accounts = db.relationship('Account', backref='user', lazy=True)

#     def __init__(self, User_Role, first_name, last_name, email, password):
#         self.first_name = first_name
#         self.last_name = last_name
#         self.email = email
#         self.password = bcrypt.generate_password_hash(password).decode('utf-8') 
#         self.User_Role = User_Role

#         print("Registered tables:", db.Model.metadata.tables.keys())

#     def __repr__(self):
#         return f"User('{self.User_Role}', '{self.first_name}', '{self.last_name}', '{self.email}')"

#     def __str__(self):
#         return f"User: {self.User_Role} ({self.first_name} {self.last_name})"


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    User_Role = db.Column(db.String(50), nullable=False)

    def __init__(self, User_Role, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')  # Hash password here
        self.User_Role = User_Role

    def __repr__(self):
        return f"User('{self.User_Role}', '{self.first_name}', '{self.last_name}', '{self.email}')"
