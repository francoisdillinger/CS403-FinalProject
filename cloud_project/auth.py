from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from .models import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.file_upload'))
            else:
                flash('Try again.', category='error')
        else:
            flash('Try again.', category='error')

    # users = User.query.all()
    # for x in users:
    #     print(f'{x.id}, {x.first_name}, {x.last_name}, {x.email}, {x.password}')
    return render_template('login.html',user=current_user)

# @auth.route('/register',methods=['GET', 'POST'])
# def register():
#     print(request.form)
#     if request.method == 'POST':
#         email = request.form.get('email')
#         firstName = request.form.get('firstname')
#         lastName = request.form.get('lastname')
#         password1 = request.form.get('password1')
#         password2 = request.form.get('password2')

#         user = User.query.filter_by(email=email).first()

#         if user:
#             flash('Email already exists .', category='error')
#         elif len(firstName) < 2:
#             flash('First name must be greater than 2 characters.', category='error')
#         elif len(lastName) < 2:
#             flash('Last name must be greater than 2 characters.', category='error')
#         elif len(email) < 4:
#             flash('Email must be greater than 4 characters.', category='error')
#         elif password1 != password2:
#             flash('Passwords don\'t match', category='error')
#         elif len(password1) < 7:
#             flash('Password must be at least 7 characters.', category='error')
#         else:
#             user = User(first_name=firstName, last_name=lastName, email=email, password=generate_password_hash(password1, method='sha256'))
#             db.session.add(user)
#             db.session.commit()
#             login_user(user, remember=True) 
#             flash('Account created!', category='success')
#             return redirect(url_for('views.home'))

#     return render_template("register.html", user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))