from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import db, UPLOAD_FOLDER
from .models import User, Recipients, Billing
from .aws_boto3_methods import aws_s3_upload
import os
import secrets


views = Blueprint('views', __name__)

@views.route('/', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        firstName = request.form.get('firstname')
        lastName = request.form.get('lastname')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists .', category='error')
        elif len(firstName) < 2:
            flash('First name must be greater than 2 characters.', category='error')
        elif len(lastName) < 2:
            flash('Last name must be greater than 2 characters.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 4 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            user = User(first_name=firstName, last_name=lastName, email=email, password=generate_password_hash(password1, method='sha256'))
            db.session.add(user)
            db.session.commit()

            flash('Account created!', category='success')
            return redirect(url_for('auth.login'))
    return render_template("register.html", user=current_user)

@views.route('/file_upload', methods=['GET','POST'])
@login_required
def file_upload():
    if request.method == 'POST':
        file = request.files['file']
        file_hex = secrets.token_hex(8)
        file_name = file_hex + file.filename
        folder_path = os.path.realpath("cloud_project") + UPLOAD_FOLDER  + file_name
        print(f'The full file path: {folder_path}')
        file.save(folder_path)
        print(f'The name of the file is: {file_name}')

        emails = []
        email1 = request.form.get('email1')
        email2 = request.form.get('email2')
        email3 = request.form.get('email3')
        email4 = request.form.get('email4')
        email5 = request.form.get('email5')

        if len(email1): emails.append(email1)
        if len(email2): emails.append(email2)
        if len(email3): emails.append(email3)
        if len(email4): emails.append(email4)
        if len(email5): emails.append(email5)

        db.session.query(Recipients).delete()
        db.session.commit()

        for email in emails:
            print(f'Email the address: {email}')
            db.session.add(Recipients(email=email))
            db.session.commit()

        aws_s3_upload(folder_path, file_name)
        db.session.add(Billing(email=current_user.email, file_name=file_name))
        db.session.commit()
 
    # print('Current User: ')
    # print(f'{current_user.id}, {current_user.first_name}, {current_user.last_name}, {current_user.email}, {current_user.password}')
    return render_template('file_upload.html', user=current_user)

@views.route('/billing', methods=['GET','POST'])
@login_required
def billing():
    bills = Billing.query.filter_by(email=current_user.email)
    # print(f'These are the bills: {bills}')
    return render_template('billing.html', bills=bills, user=current_user)