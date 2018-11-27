from wtforms import StringField, PasswordField, BooleanField, IntegerField
from wtforms.validators import *
from flask_wtf import FlaskForm
from wtforms import *



class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    firstname = StringField('Firstname', validators=[InputRequired(), Length(min=2, max=50)])
    middlename = StringField('Middle Name', validators=[InputRequired(), Length(min=2, max=50)])
    lastname = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

class addmemform(FlaskForm):
    firstname = StringField('First Name', validators=[InputRequired(), Length(min=2, max=25)])
    middlename = StringField('Middle Name', validators=[InputRequired(), Length(min=2, max=25)])
    lastname = StringField('Last Name', validators=[InputRequired(), Length(min=2, max=25)])
    birthday = StringField('Birthday', validators=[InputRequired(), Length(min=2, max=25)])
    gender = StringField('Gender', validators=[InputRequired(), Length(min=1, max=2)])

class CollectionForm(FlaskForm):
    id = IntegerField('Member ID', validators=[InputRequired()])
    capital = IntegerField('Capital', validators=[InputRequired()])
