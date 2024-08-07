import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# environment variables
load_dotenv(override=True)

app = Flask(__name__)

# sqlalchemy setup and db connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.getenv('FLASK_ENV') == 'development'
app.config['DEBUG'] = os.getenv('FLASK_ENV') == 'development'
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db = SQLAlchemy(app)
