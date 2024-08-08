from config import app, db
from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import Users
from sqlalchemy import or_


@app.route('/')
def index():
    """default route

    Returns:
        template: index.html
    """
    if 'user_id' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('login'))
    return render_template('index.html', todos=[{'task': 'Learn Flask', 'done': False}, {'task': 'Learn SQL', 'done': True}], title='Home')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """login route

    Returns:
        template: login.html
    """
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            user = Users.query.filter(
                or_(
                    Users.email == email,
                    Users.username == email
                    )).first()

            if user and user.check_password(password):
                session['user_id'] = user.id
                flash('Login successful!', 'success')
                return redirect(url_for('index'))
            else:
                flash('Invalid email or password', 'danger')
        except Exception as e:
            flash(e, 'danger')
    return render_template('login.html', title='Login')


@app.route('/about')
def about():
    """about route

    Returns:
        template: about.html
    """
    return render_template('about.html', title='About')

@app.route('/logout')
def logout():
    """Logout the user."""
    session.pop('user_id', None)
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """signup route

    Returns:
        template: signup.html
    """
    if 'user_id' in session:
        flash('You are already logged in.', 'info')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        try:
            user = Users.query.filter_by(email=email).first()
            if user:
                flash('Email already exists.', 'danger')
            elif password != confirm_password:
                flash('Passwords do not match.', 'danger')
            else:
                user = Users(email=email, username=username)
                user.password = password
                db.session.add(user)
                db.session.commit()
                flash('Account created successfully. Please log in.', 'success')
                return redirect(url_for('login'))
        except Exception as e:
            flash(e, 'danger')

    return render_template('signup.html', title='Signup')