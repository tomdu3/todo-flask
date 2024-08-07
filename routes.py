from config import app
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

@app.route('/signup')
def signup():
    """signup route

    Returns:
        template: signup.html
    """
    return render_template('signup.html', title='Signup')