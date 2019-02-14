from controller import *
from sqlalchemy.dialects import mysql
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from sqlalchemy.orm import relationship, backref

class User(UserMixin, db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    orgCode = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __init__(self, orgCode, username, password):
        self.username = username
        self.orgCode = orgCode
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.username

    def is_authenticated(self):
        return True
    def is_active(self):
        return True
    def is_anonymous(self):
        return False
    def get_id(self):
        return str(self.id)


class Member(UserMixin, db.Model):
    memberid = db.Column(db.Integer(), primary_key=True, unique=True, autoincrement=False)
    firstname = db.Column(db.String(50), nullable=False)
    middlename = db.Column(db.String(25), nullable=False)
    lastname = db.Column(db.String(25), nullable=False)
    joindate =  db.Column(db.String(200), nullable=False)
    gender = db.Column(db.String(1), nullable=False)
    mem_orgCode = db.Column(db.String(200), db.ForeignKey('organization.orgCode'), nullable=False)
    # attends = db.relationship('Attendance', backref='member', lazy=True)


    def __init__(self, memberid, firstname, middlename, lastname, joindate, gender, mem_orgCode):
        self.memberid=memberid
        self.firstname=firstname
        self.middlename=middlename
        self.lastname=lastname
        self.joindate=joindate
        self.gender=gender
        self.mem_orgCode=mem_orgCode

    def __repr__(self):
        return '<Member %r>' % self.memberid


class MemberJoin(UserMixin, db.Model):
    joinid = db.Column(db.Integer(), primary_key=True)
    memberid = db.Column(db.Integer(),db.ForeignKey('member.memberid'), unique=True, nullable=False)
    joindate =  db.Column(db.String(200), nullable=False)
    mem_orgCode = db.Column(db.String(200), db.ForeignKey('organization.orgCode'), nullable=False)
    colyear_code = db.Column(db.Integer(), db.ForeignKey('collection.colyear'), nullable=False)
    capital = db.Column(db.DECIMAL(10,2), nullable=False)
    # status = db.Column(db.String(200), nullable=False)
   


    def __init__(self, memberid, joindate, mem_orgCode, colyear_code, capital):
        self.memberid=memberid
        self.joindate=joindate
        self.mem_orgCode=mem_orgCode
        self.colyear_code=colyear_code
        self.capital=capital
        

    def __repr__(self):
        return '<MemberJoin %r>' % self.memberid

class Meeting(db.Model):
    meetingid = db.Column(db.Integer(), primary_key=True)
    meetingName = db.Column(db.String(200), unique=False, nullable=False)
    meetingDate = db.Column(db.String(200), nullable=False)
    year = db.Column(db.CHAR(4), nullable=False)
    Meeting_orgCode = db.Column(db.String(200), db.ForeignKey('organization.orgCode'), nullable=False)
    Meet_colyear = db.Column(db.Integer(), db.ForeignKey('collection.colyear'), nullable=False)
    # attendance = db.relationship('Attendance', backref='meeting', lazy=True)

    def __init__(self, meetingName, meetingDate, Meeting_orgCode, year, Meet_colyear):
        self.year = year
        self.meetingName = meetingName
        self.meetingDate = meetingDate
        self.Meeting_orgCode = Meeting_orgCode
        self.Meet_colyear = Meet_colyear


    def __repr__(self):
        return "%s" % (self.meetingName)

class Organization(db.Model):
    orgCode = db.Column(db.String(10), primary_key=True, autoincrement=False)
    orgName = db.Column(db.String(70), nullable=False, unique=True)
    meeting = db.relationship('Meeting', backref='organization', lazy=True)
    collect = db.relationship('Collection', backref='organization', lazy=True)
    attendance = db.relationship('Attendance', backref='organization', lazy=True)
    logs = db.relationship('Logs', backref='organization', lazy=True)

    def __init__(self, orgCode, orgName):
        self.orgCode=orgCode
        self.orgName=orgName
        
    def __repr__(self):
        return '<Organization %r>' %self.orgCode

class Attendance(db.Model):
    attenid = db.Column(db.Integer(), primary_key=True)
    memberid = db.Column(db.Integer(), db.ForeignKey('member.memberid'), nullable=False, unique=False)
    meetingid = db.Column(db.Integer(), db.ForeignKey('meeting.meetingid'), nullable=False)
    orgCode = db.Column(db.String(200), db.ForeignKey('organization.orgCode'), nullable=False)
    colyear = db.Column(db.Integer(), db.ForeignKey('collection.colyear'), nullable=False)
    date = db.Column(db.String(200), nullable=False)
    signin = db.Column(db.CHAR(5), nullable=True)

    def __init__(self,memberid,meetingid,date,signin,orgCode,colyear):
        self.memberid=memberid
        self.meetingid=meetingid
        self.date=date
        self.signin=signin
        self.orgCode=orgCode
        self.colyear=colyear

    def __repr__(self):
        return '<Attendance %r>' % self.id

class Collection(db.Model):
    colyear = db.Column(db.Integer(), primary_key=True, unique=True, autoincrement=False)
    colid = db.Column(db.Integer(), unique=True, autoincrement=True)
    coldate = db.Column(db.String(200), nullable=False)
    col_orgCode = db.Column(db.String(200), db.ForeignKey('organization.orgCode'), nullable=False)
    year = db.Column(db.CHAR(4), nullable=False)

    # colmeet = db.relationship('Meeting', backref='collection', lazy=True)
    # col_loan = db.relationship('Meeting', backref ='collection', lazy=True)
    # col_pay = db.relationship('Meeting', backref ='collection', lazy=True)
    # attendance = db. relationship('Meeting', backref ='collection', lazy=True)

    
    def __init__(self, colyear, coldate, col_orgCode, year):
        self.year = year
        self.colyear = colyear
        self.coldate = coldate
        self.col_orgCode = col_orgCode

    def __repr__(self):
        return ' < Collection %r>' % self.colyear

class Logs(db.Model):
    i = db.Column(db.Integer, primary_key=True)
    idno = db.Column(db.CHAR(8), nullable=False)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    dnt = db.Column(db.String(30), nullable=False)
    orgCode = db.Column(db.String(4), db.ForeignKey('organization.orgCode'), nullable=False, unique=False)

    def __init__(self, idno, fname, lname, dnt, orgCode):
        self.idno = idno
        self.fname = fname
        self.lname = lname
        self.dnt = dnt
        self.orgCode=orgCode

    def __repr__(self):
        return '<Logs %r>' % self.i
        
class Loan(db.Model):
    Loanid = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Integer(), nullable=False, unique=False)
    # interest = db.Column(db.Integer(), nullable=False, unique=False)
    # total = db.Column(db.Integer(), nullable=False, unique=False)
    loan_orgcode = db.Column(db.String(10), db.ForeignKey('organization.orgCode'), nullable=False)
    loanerid = db.Column(db.Integer(), db.ForeignKey('member_join.memberid'), nullable=True)
    loan_colyear = db.Column(db.Integer(), db.ForeignKey('collection.colyear'), nullable=False)
    status = db.Column(db.String(200), nullable=False)
    def __init__(self, date, amount, loan_orgcode, loanerid, loan_colyear,status):
        self.date = date
        self.amount = amount
        # self.interest = interest
        # self.total = total
        self.loan_orgcode = loan_orgcode
        self.loanerid = loanerid
        self.loan_colyear = loan_colyear
        self.status = status

    def __repr__(self):
        return '<Loan %r>' % self.Loanid

class Payment(db.Model):
    payid = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.String(200), nullable=False)
    amountpaid = db.Column(db.Integer(), nullable=False)
    loan_orgcode = db.Column(db.String(10), db.ForeignKey('organization.orgCode'), nullable=False)
    loanerid = db.Column(db.Integer(), db.ForeignKey('member_join.memberid'), nullable=True)
    loan_colyear = db.Column(db.Integer(), db.ForeignKey('collection.colyear'), nullable=False)
    status = db.Column(db.String(200), nullable=False)

    def __init__(self, date, amountpaid, loan_orgcode, loanerid, loan_colyear, status):
        self.date = date
        self.amountpaid = amountpaid
        self.loan_orgcode = loan_orgcode
        self.loanerid = loanerid
        self.loan_colyear = loan_colyear
        self.status = status
        
    def __repr__(self):
        return '<Payment %r>' % self.payid


        
        
    
        