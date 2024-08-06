import os
from flask import Flask, render_template
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# environment variables
load_dotenv(override=True)

app = Flask(__name__)

# sqlalchemy setup and db connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')

db = SQLAlchemy(app)

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
    app.run(debug=os.getenv('DEBUG'))
