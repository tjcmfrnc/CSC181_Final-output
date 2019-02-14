from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import *
from flask_wtf import FlaskForm
from wtforms import *
import datetime as datetime
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from models import *
from wtforms.fields.html5 import DateField, DateTimeField





class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=80)])

class RegisterForm(FlaskForm):
    orgName = StringField('Organization Name', validators=[InputRequired(), Length(min=4, message="Invalid input")])
    orgCode = StringField('Organization Code', validators=[InputRequired(), Length(min=4, message="Invalid input")])
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=3, max=80)])

class addmemform(FlaskForm):
    memberid = IntegerField('ID number', validators=[InputRequired()])
    firstname = StringField('Firstname', validators=[InputRequired(), Length(min=2, max=25)])
    middlename = StringField('Middlename', validators=[InputRequired(), Length(min=2, max=25)])
    lastname = StringField('Lastname', validators=[InputRequired(), Length(min=2, max=25)])
    gender = SelectField(u'Sex', choices=[('M', 'M'), ('F', 'F')], validators=[InputRequired()])


class newMeeting(FlaskForm):
    meetingName = StringField('Meeting Name', validators=[InputRequired(), Length(min=5,max=200, message='Invalid input')])


class UpMeeting(FlaskForm):
    meetingName = StringField('Meeting Name', validators=[InputRequired(), Length(min=5, max=200, message='Invalid input')])

class DelMeeting(FlaskForm):
    meetingid = StringField('Meeting ID', validators=[InputRequired(), Length(min=4,max=4, message='Invalid event code')])

class NewAttendance(FlaskForm):
    memberid = IntegerField('Member ID', validators=[InputRequired()])
    attendtype = SelectField(u'Attendance Type', choices=[('IN', 'Sign In')])

class AdminAttendance(FlaskForm):
    mee_name = QuerySelectField('Meeting',query_factory=lambda: Meeting.query,allow_blank=False)
    memberid = IntegerField('Member ID', validators=[InputRequired()])
    attendtype = SelectField(u'Attendance Type', choices=[('IN', 'Sign In')])

class addLoan(FlaskForm):
    memberid = IntegerField('Active-Members',validators=[InputRequired()])
    date = DateField('Date', format='%Y-%m-%d')
    amount = IntegerField('Amount', validators=[InputRequired()])


class NewCollection(FlaskForm):
    colyear = SelectField(u'Collection Year', choices=[('2018','2018'), ('2019','2019'), ('2020','2020'),
                                                      ('2021', '2021'), ('2022','2022'), ('2023','2023'),
                                                      ('2024', '2024'), ('2025','2025')], validators=[InputRequired()])



class JoinMember(FlaskForm):
    memid = IntegerField('Member ID',validators=[InputRequired()])
    capital = DecimalField('Amount', validators=[InputRequired()], default=0)
    

class Loan(FlaskForm):
    memid = IntegerField('Member ID',validators=[InputRequired()])
    amount = DecimalField('Amount', validators=[InputRequired()], default=0)

class UPuser(FlaskForm):
    username = StringField('New Username', validators=[InputRequired()])
    password = PasswordField('New Password', validators=[InputRequired()])

class Pay(FlaskForm):
    loanerid = IntegerField('Member ID', validators=[InputRequired()])
    amount = IntegerField('Amount', validators=[InputRequired()])
    attendtype = SelectField(u'Status', choices=[('Paid', 'Pay')])

class Newloan(FlaskForm):
    memberid = IntegerField('Student ID', validators=[InputRequired()])
    amount = IntegerField('Amount', validators=[InputRequired()])
    attendtype = SelectField(u'Status', choices=[('Unpaid', 'Loan')])

class Payloan(FlaskForm):
    attendtype = SelectField(u'validate', choices=[('Paid', 'Payment Received')])