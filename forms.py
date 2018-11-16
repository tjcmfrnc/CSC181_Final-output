from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import *
from flask_wtf import FlaskForm
from wtforms import *



class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    firstname = StringField('firstname', validators=[InputRequired(), Length(min=2, max=50)])
    middlename = StringField('middlename', validators=[InputRequired(), Length(min=2, max=50)])
    lastname = StringField('lastname', validators=[InputRequired(), Length(min=2, max=50)])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class addmemform(FlaskForm):
    firstname = StringField('firstname', validators=[InputRequired(), Length(min=2, max=25)])
    middlename = StringField('middlename', validators=[InputRequired(), Length(min=2, max=25)])
    lastname = StringField('lastname', validators=[InputRequired(), Length(min=2, max=25)])
    birthday = StringField('birthday', validators=[InputRequired(), Length(min=2, max=25)])
    gender = StringField('gender', validators=[InputRequired(), Length(min=1, max=2)])
    capital = StringField('capital', validators=[InputRequired(), Length(min=2, max=25)])