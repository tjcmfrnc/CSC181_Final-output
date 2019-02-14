from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask import Flask, render_template, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from sqlalchemy import join
import os 
from controller import *
from models import *
from forms import *
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector
from datetime import timedelta
from models import Collection
from models import Loan
import calendar



createDB()
createTables()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login2'


@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except User.DoesNotExist:
        return None

@login_manager.unauthorized_handler
def unauthorized():
    flash('Admin rights needed to access this page')
    return redirect(url_for('login2'))


@app.route('/', methods=['POST','GET'])
def index():
    form = LoginForm()
    msgs = ""
    name = db.session.query(Organization.orgName).first()
    if request.method=='POST' and form.validate_on_submit():
        username = User.query.filter_by(username=form.username.data).first()
        try:
            if username.username == form.username.data:
                    if check_password_hash(username.password, form.password.data):
                        login_user(username, remember=True)
                    return redirect(url_for('adminhomepage'))
            else:
                msgs = "Username or password is invalid"
                return render_template('index2.html', form=form, name=name, msgs=msgs)
        except:
            msgs = 'Setup a User First!'
            return render_template('index2.html', form=form, name=name, msgs=msgs)
    return render_template('index2.html', form=form, name=name, msgs=msgs)


@app.route('/userinfo')
@login_required
def userinfo():
    user = User.query.all()
    org = Organization.query.all()
    return render_template('userinfo.html', name=current_user.username, user=user, org=org)

@app.route('/deleteuser/<int:id>', methods=['GET', 'POST'])
def deleteuser(id):
    form = UPuser()
    msgs =''
    if request.method=='POST' and form.validate_on_submit():
        check = User.query.filter_by(id=id).first()
        if check is None:
            msgs = 'User does not exist!'
            return render_template('user_update.html', form=form, msgs=msgs)
        elif check.id == id:
            check.username = form.username.data
            check.password = generate_password_hash(form.password.data)
            db.session.commit()
            flash(' Record changes saved successfully!')
            return redirect(url_for('index'))
    return render_template('user_update.html', form=form, msgs=msgs, id=id)


@app.route('/signup2', methods=['GET','POST'])
def signup2():
    form = RegisterForm()
    check = Organization.query.first()
    if check is None:
        if request.method=='POST' and form.validate_on_submit():
            db.session.add(User(username=form.username.data, password=generate_password_hash(form.password.data), orgCode=form.orgCode.data))
            db.session.add(Organization(orgCode=form.orgCode.data, orgName=form.orgName.data))
            db.session.commit()
            flash(" Success! You have created an admin account!")
            return redirect(url_for('index'))
    else:
        return render_template('error.html')
    return render_template('signup2.html', form=form)



@app.route('/addmember3', methods = ['GET','POST'])
def addmember3():
    now = datetime.datetime.now()
    form = addmemform()
    if form.validate_on_submit():
        memid = form.memberid.data
        fname = form.firstname.data
        mname = form.middlename.data
        lname = form.lastname.data
        member = Member.query.filter_by(memberid=memid).first()
        if member is None:

            new_member = Member(memberid=memid, firstname=fname, middlename=mname, lastname=lname, joindate = now, gender = form.gender.data,
                                  mem_orgCode=current_user.orgCode)
            db.session.add(new_member)
            db.session.commit()
            flash('Member created successfully!')
            return render_template('adminhomepage.html', form=form)
        else:
            flash('Member already exist!')

    return render_template('addmember3.html', form=form)

@app.route('/deletemember/<int:memberid>', methods=['GET','POST'])
def deletemember(memberid):
    try:
        Member.query.filter_by(memberid=memberid).delete()
        db.session.commit()
        flash(' Member removed successfully!')
        return redirect(url_for('member'))
    except:
        flash(' Cannot delete Member who joined current collection year!')
        query = MemberJoin.query.filter_by(mem_orgCode=current_user.orgCode).order_by(MemberJoin.joindate)
        return render_template('adminhomepage.html', query=query)

@app.route('/joinmember', methods=['GET', 'POST'])
@login_required
def joinmember():
    now = datetime.datetime.now()
    form = JoinMember()

    if request.method=='POST' and form.validate_on_submit():
        exist = MemberJoin.query.filter_by(memberid=form.memid.data).first()
        try:
            if not exist:
                new_jmem = MemberJoin(memberid=form.memid.data, capital=form.capital.data, joindate=now, mem_orgCode=current_user.orgCode, colyear_code=now.year)
                db.session.add(new_jmem)
                db.session.commit()
                flash(' Member successfully Activated!')
                return redirect(url_for('activemember'))
            else:
                flash('Member already exist!')
            return redirect(url_for('Joinmember'))
        except:
            flash(' Member does not exist!')
            return redirect(url_for('joinmember'))
        
    return render_template('joinmember.html', form=form)

@app.route('/activemember')
@login_required
def activemember():
    now = datetime.datetime.now()
    member = MemberJoin.query.filter(MemberJoin.joindate >= now.year).order_by(MemberJoin.joindate)
    capital = MemberJoin.query.all()
    total_revenue = 0
    for i in capital:
        total_revenue = i.capital * 3

    return render_template('activemember.html', name=current_user.username, MemberJoin=member, capital=total_revenue)

@app.route('/pastactivemember')
@login_required
def pastactivemember():
    now = datetime.datetime.now()
    member = MemberJoin.query.filter(MemberJoin.joindate < now.year).order_by(MemberJoin.joindate)  # reference
    return render_template('activemember_past.html', MemberJoin=member)

@app.route('/adminhomepage')
@login_required
def adminhomepage():
    msgs = 'Hello there, ' + str(current_user.username) + '!'
    return render_template('adminhomepage.html', name=current_user.username, msgs=msgs)

@app.route('/member')
@login_required
def member():
    member = Member.query.all()
    return render_template('member.html', name=current_user.username, member=member)

@app.route('/loan')
@login_required
def loan():
    now = datetime.datetime.now()
    loan = Loan.query.filter(Loan.loan_colyear >= now.year).order_by(Loan.Loanid)
    pay = Payment.query.all()
    my_status = 0
    for i in pay:
        my_status = i.status

    return render_template('loan.html', name=current_user.username, query=loan, my_status=pay)

@app.route('/pastloan')
@login_required
def pastloan():
    now = datetime.datetime.now()
    loan = Loan.query.filter(Loan.loan_colyear < now.year).order_by(Loan.Loanid)
    return render_template('loan_past.html', name=current_user.username, query=loan)

@app.route('/addloan', methods=['GET','POST'])
@login_required
def addloan():
    form = Newloan(loan_orgCode=current_user.orgCode)
    now = datetime.datetime.now()
    if request.method=='POST' and form.validate_on_submit():
        exist = MemberJoin.query.filter_by(memberid=form.memberid.data).first()
        if exist:
            db.session.add(Loan(amount=form.amount.data, date=now, status=form.attendtype.data,
                                    loan_orgcode=current_user.orgCode, loanerid=form.memberid.data, loan_colyear=now.year))
            db.session.commit()
            flash(' Record successfully added!')
            return redirect(url_for('loan'))
        else:
            flash('Member is NOT active')
            return redirect(url_for('addloan'))
    return render_template('loan_add.html', form=form)
    



@app.route('/newmeeting', methods=['GET','POST']) #DONE
@login_required
def newmeeting():
    form = newMeeting()
    now = datetime.datetime.now()
    if request.method=='POST' and form.validate_on_submit():
        meeting = Meeting.query.filter_by(meetingDate=now).first()
        if meeting is None:
            db.session.add(Meeting(meetingName=form.meetingName.data, meetingDate=now, Meeting_orgCode=current_user.orgCode, Meet_colyear=now.year, year=now.year))
            db.session.commit()
            flash(" Success! You have created a meeting!")
            return redirect(url_for('meeting'))
        else:
            flash('Meeting already exist!')
    return render_template('newmeeting.html', form=form)

@app.route('/meeting', methods=['GET', 'POST'])
@login_required
def meeting():
    now = datetime.datetime.now()
    query = Meeting.query.filter(Meeting.year >= now.year).order_by(Meeting.meetingDate)
    return render_template('meeting.html', query=query)

@app.route('/pastmeeting')
@login_required
def pastmeeting():
    now = datetime.datetime.now()
    query = Meeting.query.filter(Meeting.year < now.year).order_by(Meeting.year)  # reference
    return render_template('meeting_past.html', query=query)

@app.route('/updatemeeting/<int:meetingid>', methods=['GET', 'POST'])
def updatemeeting(meetingid):
    now = datetime.datetime.now()
    form = UpMeeting()
    msgs =''
    if request.method=='POST' and form.validate_on_submit():
        check = Meeting.query.filter_by(meetingid=meetingid).first()
        if check is None:
            msgs = 'Meeting does not exist!'
            return render_template('meeting_update.html', form=form, msgs=msgs)
        elif check.meetingid == meetingid:
            check.meetingName = form.meetingName.data
            db.session.commit()
            flash(' Record changes saved successfully!')
            return redirect(url_for('meeting'))
    return render_template('meeting_update.html', form=form, msgs=msgs, meetingid=meetingid)


@app.route('/deletemeeting/<int:meetingid>', methods=['GET','POST'])
def deletemeeting(meetingid):
    try:
        Meeting.query.filter_by(meetingid=meetingid).delete()
        db.session.commit()
        flash(' Meeting removed successfully!')
        return redirect(url_for('meeting'))
    except:
        flash(' Cannot delete meeting that have existing attendance records!')
        query = Meeting.query.filter_by(Meeting_orgCode=current_user.orgCode).order_by(Meeting.meetingDate)
        return render_template('meeting.html', query=query)


@app.route('/collection', methods=['GET', 'POST'])
@login_required
def collection():
    now = datetime.datetime.now()
    total = MemberJoin.query.all()
    total2 = Payment.query.all()
    total3 = Loan.query.all()
    total_capital = 0
    for i in total:
        total_capital += i.capital

    total_payment = 0
    for i in total2:
        total_payment += i.amountpaid

    total_loan = 0
    for i in total3:
        total_loan += i.amount

    final = total_capital + total_payment
    capital = total_capital - total_loan
    revenue = capital + total_payment
    capital2 = revenue
    paid = total_loan - total_payment

    query = Collection.query.filter(Collection.colyear >= now.year).order_by(Collection.year)
    return render_template('collection.html', query=query,total=total_capital, capital2=capital2, total2=total_payment, total3=total_loan, revenue=revenue, paid=paid)

@app.route('/pastcollection')
@login_required
def pastcollection():
    now = datetime.datetime.now()
    query = Collection.query.filter(Collection.year < now.year).order_by(Collection.year)  # reference
    return render_template('collection_past.html', query=query)

@app.route('/newcollection', methods=['GET','POST']) #DONE
@login_required
def newcollection():
    now = datetime.datetime.now()
    form = NewCollection()
    if request.method=='POST' and form.validate_on_submit():
        collection = Collection.query.filter_by(year=now.year).first()
        if collection is None:
            
            db.session.add(Collection(colyear=form.colyear.data, coldate=now, col_orgCode=current_user.orgCode, year=now.year))
            db.session.commit()
            flash(" Success! You have added a new collection!")
            return redirect(url_for('collection'))
        else:
            flash('Collection already exist!')
    return render_template('addcollection.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/attendance',methods=['POST', 'GET']) #datatables
@login_required
def attendance():
    form = AdminAttendance()
    if request.method=='POST' and form.validate_on_submit():
        now=datetime.datetime.now()
        query = Meeting.query.filter_by(meetingName=str(form.mee_name.data)).first()
        check = Attendance.query.filter_by(memberid=form.memberid.data, meetingid=query.meetingid).first()
        member = Member.query.filter_by(memberid=form.memberid.data).first()
        if member is None:
            flash(' Student does not exist!')
            return render_template('attendance.html', form=form)
        if check is None:
            if form.attendtype.data == 'IN':
                db.session.add(Attendance(memberid=form.memberid.data, meetingid=query.meetingid, date=now.strftime("%Y-%m-%d %H:%M"),
                                          signin=form.attendtype.data, orgCode=current_user.orgCode, colyear=now.year))
                db.session.commit()
                flash(' Student recorded successfully!')
                return render_template('attendance.html',form=form)
        elif check.memberid == form.memberid.data:
            if form.attendtype.data == 'IN':
                check.signin = form.attendtype.data
                db.session.commit()
                flash(' Student recorded successfully!')
                return render_template('attendance.html',form=form)
    return render_template('attendance.html', form=form)

@app.route('/newattendance/<int:meetingid>/<meetingDate>', methods=['GET', 'POST'])
@login_required
def newattendance(meetingid, meetingDate):
    form = NewAttendance()
    msgs = ""
    if request.method=='POST' and form.validate_on_submit():
        now=datetime.datetime.now()
        check = Attendance.query.filter_by(memberid=form.memberid.data, meetingid=meetingid).first()
        query = Member.query.filter_by(memberid=form.memberid.data).first()
        if query is None:
            msgs = 'Student does not exist!'
            return render_template('attendance_new.html', meetingid=meetingid, form=form, meetingDate=meetingDate, msgs=msgs)
        if check is None:
            if form.attendtype.data=='IN':
                db.session.add(Attendance(memberid=form.memberid.data, meetingid=meetingid, signin=form.attendtype.data, date=now.strftime("%Y-%m-%d %H:%M"),
                                          orgCode=current_user.orgCode, colyear=now.year))
                db.session.commit()
                flash(' Student recorded successfully!')
                return redirect(url_for('newattendance', meetingid=meetingid, meetingDate=meetingDate))

        elif check.memberid == form.memberid.data and check.meetingid==meetingid:
            if form.attendtype.data == 'IN':
                check.signin = form.attendtype.data
                db.session.commit()
                flash(' Student recorded successfully!')
                return render_template('attendance_new.html', meetingid=meetingid, form=form, meetingDate=meetingDate, msgs=msgs)
    return render_template('attendance_new.html', meetingid=meetingid, form=form, meetingDate=meetingDate, msgs=msgs)

            

@app.route('/attendancelist/<int:meetingid>/')
@login_required
def attendancelist(meetingid):
    check = Meeting.query.filter_by(meetingid=meetingid).first()
    query = db.session.query(Attendance.signin, Attendance.memberid,
                             Member.firstname, Member.lastname, Attendance.date).outerjoin(Member, Meeting).filter_by(meetingid=meetingid).order_by(Member.lastname)

    return render_template('attendance_list.html', meetingid=meetingid, query=query, check=check)

@app.route('/adminlogs/')
@login_required
def adminlogs():
    query = Logs.query.filter_by(orgCode=current_user.orgCode)
    return render_template('logs.html', query=query)

@app.route('/loan_details/<int:id>', methods=['GET', 'POST'])
def load_details(id):
    lquery = Loan.query.filter_by(loanerid = id).first()
    loandate = lquery.date
    print loandate
    today = datetime.datetime.now()
    amount = lquery.amount
    days_in_month = 30
    ty = today.strftime('%Y')
    td = today.strftime('%d')
    tm = today.strftime('%m')

    ly = loandate[0:4]
    print ly
    lm = loandate[5:7]
    print lm
    ld = loandate[8:10]
    print ld


    tod = datetime.date(int(ty), int(tm), int(td))
    lod = datetime.date(int(ly), int(lm), int(ld))
    print tod
    print lod
    diff = tod - lod
    print diff.days
    inter = 0.10
    mult = diff.days/days_in_month
    percentage = inter*mult
    interest = amount * percentage
    total = amount + interest
    
    return render_template("loan_details.html",amount = amount, today = today, total = total, interest = interest, percentage = percentage)

# @app.route('/payment')
# @login_required
# def payment():
#     query = Loan.query.filter_by(orgCode=current_user.orgCode)
#     return render_template('logs.html', query=query)
@app.route('/payment', methods=['GET', 'POST'])
@login_required
def payment():
    form = Pay()
    msgs = ""
    if request.method=='POST' and form.validate_on_submit():
        now=datetime.datetime.now()
        query = MemberJoin.query.filter_by(memberid=form.loanerid.data).first()
        check = Payment.query.filter_by(loanerid=form.loanerid.data).first()
        if query is None:
            msgs = 'Student does not exist!'
            return render_template('payment.html', form=form, msgs=msgs)
        if check is None:
            if form.attendtype.data=='Paid':
                db.session.add(Payment(loanerid=form.loanerid.data, status=form.attendtype.data, date=now,
                                          loan_orgcode=current_user.orgCode, loan_colyear=now.year, amountpaid=form.amount.data))
                db.session.commit()
                flash(' Payment recorded successfully!')
                return redirect(url_for('paymentview'))

        elif check.loanerid == form.loanerid.data:
            if form.attendtype.data == 'Paid':
                check.pay = form.attendtype.data
                db.session.commit()
                flash(' Student recorded successfully!')
                return render_template('payment.html', form=form, msgs=msgs)
    return render_template('payment.html', form=form, msgs=msgs)

@app.route('/paymentview', methods=['GET', 'POST'])
@login_required
def paymentview():
    now = datetime.datetime.now()
    query = Payment.query.filter(Payment.loan_colyear >= now.year).order_by(Payment.date)
    return render_template('payment_view.html', query=query)




@app.route('/newloan', methods=['GET', 'POST'])
@login_required
def newloan():
    now = datetime.datetime.now()
    form = Newloan()
    msgs = ""
    if request.method=='POST' and form.validate_on_submit():
        check = Loan.query.filter_by(loanerid=form.memberid.data).first()
        query = MemberJoin.query.filter_by(memberid=form.memberid.data).first()
        if query is None:
            msgs = 'Student does not exist!'
            return render_template('loan_add.html',form=form, msgs=msgs)
        if check is None:
            if form.attendtype.data=='Unpaid':
                db.session.add(Loan(loanerid=form.memberid.data, amount=form.amount.data, loan_colyear=now.year, date=now, status=form.attendtype.data,
                                        loan_orgcode=current_user.orgCode))
                db.session.commit()
                flash(' Student recorded successfully!')
                return redirect(url_for('newloan'))
            if form.attendtype.data=='Paid':
                db.session.add(Loan(loanerid=form.memberid.data, amount=form.amount.data, loan_colyear=now.year, date=now, status=form.attendtype.data,
                                        loan_orgcode=current_user.orgCode))
                db.session.commit()
                flash(' Student recorded successfully!')
                return render_template('loan_add.html', form=form, msgs=msgs)
        elif check.loanerid == form.memberid.data:
            if form.attendtype.data == 'Unpaid':
                check.signin = form.attendtype.data
                db.session.commit()
                flash(' Student recorded successfully!')
                return render_template('loan_add.html',form=form,msgs=msgs)
            if form.attendtype.data == 'Paid':
                check.signout = form.attendtype.data
                db.session.commit()
                flash(' Student recorded successfully!')
                return render_template('loan.html',form=form, msgs=msgs)
    return render_template('loan_add.html',form=form, msgs=msgs)

@app.route('/payloan/<int:Loanid>', methods=['GET', 'POST'])
def payloan(Loanid):
    now = datetime.datetime.now()
    form = Payloan()
    msgs =''
    if request.method=='POST' and form.validate_on_submit():
        check = Loan.query.filter_by(Loanid=Loanid).first()
        if check is None:
            msgs = 'Loan does not exist!'
            return render_template('loan_pay.html', form=form, msgs=msgs)
        elif check.Loanid == Loanid:
            check.status = form.attendtype.data
            db.session.commit()
            flash(' Record changes saved successfully!')
            return redirect(url_for('loan'))
    return render_template('loan_pay.html', form=form, msgs=msgs, Loanid=Loanid, now=datetime.datetime.now())

@app.route('/newpayment', methods=['GET','POST'])
@login_required
def newpayment():
    form = Pay(loan_orgCode=current_user.orgCode)
    now = datetime.datetime.now()
    if request.method=='POST' and form.validate_on_submit():
        exist = Loan.query.filter_by(loanerid=form.loanerid.data).first()
        if exist:
            db.session.add(Payment(amountpaid=form.amount.data, date=now, status=form.attendtype.data,
                                    loan_orgcode=current_user.orgCode, loanerid=form.loanerid.data, loan_colyear=now.year))
            db.session.commit()
            flash(' Record successfully added!')
            return redirect(url_for('paymentview'))
        else:
            flash('Member is NOT active')
            return redirect(url_for('newpayment'))
    return render_template('payment.html', form=form)

# @app.route('/distribute', methods=['GET','POST'])
# @login_required
# def distribute():
#     now = datetime.datetime.now()
#     member = MemberJoin.query.filter(MemberJoin.joindate >= now.year).order_by(MemberJoin.joindate)
#     # loan = Loan.query.filter(Loan.loanerid)
#     # total_capital = 0
#     # for i in loan:
#     #     total_capital = i.amount

#     return render_template('activemember.html', name=current_user.username, MemberJoin=member)


if __name__ == '__main__':
    app.run(debug=True)

