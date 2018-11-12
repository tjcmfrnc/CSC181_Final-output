from flask import Flask, render_template, redirect, url_for
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:password@localhost/testdb3'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


def createDB():
    engine = sqlalchemy.create_engine('mysql://root:password@localhost')# connects to server
    engine.execute("CREATE DATABASE IF NOT EXISTS testdb") #create db
    engine.execute("USE testdb") # select new

def createTables():
    db.create_all()


#_________________________________TABLES________________________________________
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
    capital = db.Column(db.Integer)


#________________________________________________________________________________
createTables()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('adminhomepage'))
            else:
                flash('Invalid username or password!')

        return '<h1>Invalid username or password</h1>'
        return render_template('index.html')
        #return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'

    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    admin = User.query.all()
    count = 1
    for i in admin:
        if count >= 1:
            #flash('Admin already setup!')
            return render_template("index.html")
        count+=1

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(firstname=form.firstname.data, middlename=form.middlename.data, lastname=form.lastname.data, username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
    return render_template('signup.html', form=form)

    #return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    #return render_template('signup.html', form=form)

@app.route('/addmember', methods = ['GET','POST'])
def addmember():
    form = addmemform()
    if form.validate_on_submit():
        fname = form.firstname.data
        mname = form.middlename.data
        lname = form.lastname.data
        Member = Members.query.filter_by(firstname=fname, middlename=mname, lastname=lname, birthday = form.birthday.data, gender = form.gender.data).first()
        if Member is None:

            new_member = Members(firstname=fname, middlename=mname, lastname=lname, birthday = form.birthday.data, gender = form.gender.data, capital = form.capital.data)
            db.session.add(new_member)
            db.session.commit()
            flash('member created successfully!')
            return render_template('adminhomepage.html', form=form)
        else:
            flash('member already exist!')

    return render_template('addmember.html', form=form)

@app.route('/adminhomepage')
@login_required
def adminhomepage():
    msgs = 'Hello there, ' + str(current_user.username) + '!'
    return render_template('adminhomepage.html', name=current_user.username, msgs=msgs)

@app.route('/members')
@login_required
def members():
    members = Members.query.all()
    total = 0
    t = 0
    for member in members:
        total += member.capital
        t += member.id
    return render_template('members.html', name=current_user.username,members=members, total=total, t=t)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)