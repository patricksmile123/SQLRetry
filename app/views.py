import traceback

from flask import render_template, redirect, url_for, flash
from app import app, db
from datetime import datetime
from app.forms import LoginForm, RegistrationForm, AddStudentForm, LoanForm
from app.models import Student, Loan


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/datetime')
def date_time():
    now = datetime.now()
    return render_template('datetime.html', title='Date & Time', now=now)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash(f'Login for {form.username.data}', 'success')
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Registration for {form.username.data} received', 'success')
        return redirect(url_for('index'))
    return render_template('registration.html', title='Register', form=form)


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    form = AddStudentForm()
    if form.validate_on_submit():
        new_student = Student(username=form.username.data, firstname=form.firstname.data,
                              lastname=form.lastname.data, email=form.email.data)
        db.session.add(new_student)
        try:
            db.session.commit()
            flash(f'New Student added: {form.username.data} received', 'success')
            return redirect(url_for('index'))
        except:
            db.session.rollback()
            if Student.query.filter_by(username=form.username.data).first():
                form.username.errors.append('This username is already taken. Please choose another')
            if Student.query.filter_by(email=form.email.data).first():
                form.email.errors.append('This email address is already registered. Please choose another')
    return render_template('add_student.html', title='Add Student', form=form)


@app.route('/borrow_device', methods=['GET', 'POST'])
def borrow_device():
    form = LoanForm()
    if form.validate_on_submit():
        new_loan = Loan(device_id=form.device_id.data, student_id=form.student_id.data, borrowdatetime=datetime.now(),)
        db.session.add(new_loan)
        try:
            db.session.commit()
            flash(f'Borrow Received', 'success')
            return redirect(url_for('index'))
        except Exception:
            print(traceback.format_exc())
            db.session.rollback()
            if Loan.query.filter_by(device_id=form.device_id.data).first():
                form.device_id.errors.append('This device is already taken!')
            if Loan.query.filter_by(student_id=form.student_id.data).first():
                form.student_id.errors.append('This student already has a device taken out')
    return render_template('loan.html', title='Borrow Device', form=form)
