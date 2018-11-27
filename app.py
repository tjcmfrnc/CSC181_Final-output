from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from controller import *
from models import *
from forms import *
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

createDB()
createTables()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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

        #return '<h1>Invalid username or password</h1>'
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
            return render_template("error.html")
        count+=1

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(firstname=form.firstname.data, middlename=form.middlename.data, lastname=form.lastname.data, username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()


        return '<h1>New user has been created!</h1>'
        #return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'

    return render_template('signup.html', form=form)

@app.route('/addmember', methods = ['GET','POST'])
def addmember():
    form = addmemform()
    if form.validate_on_submit():
        fname = form.firstname.data
        mname = form.middlename.data
        lname = form.lastname.data
        Member = Members.query.filter_by(firstname=fname, middlename=mname, lastname=lname, birthday = form.birthday.data, gender = form.gender.data).first()
        if Member is None:
            new_member = Members(firstname=fname, middlename=mname, lastname=lname, birthday = form.birthday.data, gender = form.gender.data)
            db.session.add(new_member)
            db.session.commit()
            flash('Member Created Successfully!')
            return render_template('adminhomepage.html', form=form)
        else:
            flash('Member Already Exist!')

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
        t += member.id
    return render_template('members.html', name=current_user.username,members=members, total=total, t=t)

@app.route('/add_collection', methods=['GET','POST'])
@login_required
def collection():
    form = CollectionForm()

    # if form.validate_on_submit():
    if request.method == 'POST':
        # print"wizzzzzzzzzzzzzzzzzzz"
        capital = form.capital.data
        # print str(capital)+"----------------------------------------------"
        new_capital = Collection(capital=capital)
        db.session.add(new_capital)
        db.session.commit()
        flash('Capital Added!')
        return render_template('adminhomepage.html')  
    return render_template('add_collection.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)