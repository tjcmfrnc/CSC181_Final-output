from controller import *
from sqlalchemy.dialects import mysql
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    middlename = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(15), unique=True)
    password = db.Column(db.String(80))


class Members(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(25))
    middlename = db.Column(db.String(25))
    lastname = db.Column(db.String(25))
    birthday = db.Column(db.String(25))
    gender = db.Column(db.String(1))
    

class Collection(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    capital = db.Column(db.Integer())