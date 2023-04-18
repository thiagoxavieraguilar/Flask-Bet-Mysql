from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash


auth = Blueprint("auth", __name__)


@auth.route("/login", methods=['GET','POST'])
def login():
    if request.method == 'POST':
        #get the email and password from the request form
        email = request.form.get("email")
        password = request.form.get("password")
        #check if user exist in the database
        user = User.query.filter_by(email=email).first()
        if user:
            #check password matches the hashed password in the databas
            if check_password_hash(user.password, password):
                #if the password is correct, log the user in and redirect them to the home page
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                #if the password is incorrect, show an error message
                flash('Password is incorrect.', category='error')
        else:
            #if email does not exist, show an error message
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route("/sign-up", methods=['GET','POST'])
def sign_up():
    #get the email, username, password, and password confirmation from the request form
    if request.method == 'POST':
        email = request.form.get("email")
        username = request.form.get("username")
        password = request.form.get("password")
        confirm_password = request.form.get("confirm_password")
        
        #check if the email or username already exists in the database
        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()

        #validate the input
        if email_exists:
            flash('Email is already in use.', category='error')
        elif username_exists:
            flash('Username is already in use.', category='error')
        elif password != confirm_password:
            flash('Password don\'t match!', category='error')
        elif len(username) < 2:
            flash('Username is too short.', category='error')
        elif len(password) < 6:
            flash('Password is too short.', category='error')
        elif len(email) < 4:
            flash("Email is invalid.", category='error')
        else:
            #if the input is valid, create a new user, log them in, and redirect them to the home page
            new_user = User(email=email, username=username, password=generate_password_hash(password, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('User created!')
            return redirect(url_for('views.home'))  
    
    return render_template("signup.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))