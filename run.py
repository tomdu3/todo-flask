from config import app
from flask import render_template, request
from models import Users


@app.route('/')
def index():
    """default route

    Returns:
        template: index.html
    """
    return render_template('index.html', todos=[{'task': 'Learn Flask', 'done': False}, {'task': 'Learn SQL', 'done': True}], title='Home')


@app.route('/login')
def login():
    """login route

    Returns:
        template: login.html
    """
    return render_template('login.html', title='Login')


@app.route('/about')
def about():
    """about route

    Returns:
        template: about.html
    """
    return render_template('about.html', title='About')

@app.route('/signup')
def signup():
    """signup route

    Returns:
        template: signup.html
    """
    return render_template('signup.html', title='Signup')




if __name__ == '__main__':
    app.run()
