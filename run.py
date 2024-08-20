import os
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy import or_
from sqlalchemy.sql import func, false
import bcrypt
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv(override=True)

# Configuration
class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('FLASK_ENV') == 'development'
    DEBUG = os.getenv('FLASK_ENV') == 'development'
    SECRET_KEY = os.getenv('SECRET_KEY')

# Initialize the app, database, and migration objects
app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Models
class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    _password = db.Column('password', db.String(120), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    def __repr__(self):
        return f'<User {self.username} {self.id}>'

    @property
    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at
        }

    @property
    def password(self):
        raise AttributeError('password is not readable')

    @password.setter
    def password(self, plaintext_password):
        if not isinstance(plaintext_password, str):
            raise TypeError("Password must be a string")

        hashed_password = bcrypt.hashpw(
            plaintext_password.encode('utf-8'),
            bcrypt.gensalt()
        )
        self._password = hashed_password.decode('utf-8')

    def check_password(self, plaintext_password):
        return bcrypt.checkpw(
            plaintext_password.encode('utf-8'),
            self._password.encode('utf-8')
        )

class Todo(db.Model):
    __tablename__ = 'Todo'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    done = db.Column(db.Boolean, default=False, server_default=false())
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __init__(self, title, user_id, done=None):
        self.title = title
        self.user_id = user_id
        self.done = done if done is not None else False

    def __repr__(self):
        return f'<Todo {self.title} {self.id}>'

# Routes
@app.route("/")
def index():
    if "user_id" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login"))
    
    user = User.query.get(session["user_id"])
    if not user:
        flash("User not found.", "danger")
        return redirect(url_for("logout"))

    todos = Todo.query.filter_by(user_id=session["user_id"]).all()
    todos = sorted(todos, key=lambda x: x.created_at)
    return render_template("index.html", todos=todos, username=user.username, title="Home")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        try:
            user = User.query.filter(or_(User.email == email, User.username == email)).first()
            if user and user.check_password(password):
                session["user_id"] = user.id
                flash("Login successful!", "success")
                return redirect(url_for("index"))
            else:
                flash("Invalid email or password", "danger")
        except Exception as e:
            flash(str(e), "danger")
    return render_template("login.html", title="Login")

@app.route("/about")
def about():
    return render_template("about.html", title="About")

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if "user_id" in session:
        flash("You are already logged in.", "info")
        return redirect(url_for("index"))

    if request.method == "POST":
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]

        try:
            user = User.query.filter_by(email=email).first()
            if user:
                flash("Email already exists.", "danger")
            elif password != confirm_password:
                flash("Passwords do not match.", "danger")
            else:
                user = User(email=email, username=username)
                user.password = password
                db.session.add(user)
                db.session.commit()
                flash("Account created successfully. Please log in.", "success")
                return redirect(url_for("login"))
        except Exception as e:
            flash(str(e), "danger")

    return render_template("signup.html", title="Signup")

@app.route("/create-task", methods=["GET", "POST"])
def create_task():
    if "user_id" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form["title"]

        try:
            todo = Todo(title=title.title(), user_id=session["user_id"])
            db.session.add(todo)
            db.session.commit()
            flash("Task created successfully!", "success")
            return redirect(url_for("index"))
        except Exception as e:
            flash(str(e), "danger")

    return render_template("create-task.html", title="Create Task")

@app.route("/update_task/<int:todo_id>", methods=["GET", "POST"])
def update_task(todo_id):
    if "user_id" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login"))

    todo = Todo.query.filter_by(id=todo_id, user_id=session["user_id"]).first_or_404()
    if request.method == "POST":
        todo.title = request.form["title"]

        try:
            db.session.commit()
            flash("Task updated successfully!", "success")
            return redirect(url_for("index"))
        except Exception as e:
            db.session.rollback()  # Rollback in case of an error
            flash("An error occurred: " + str(e), "danger")

    return render_template("update-task.html", todo=todo, title="Update Task")
    if "user_id" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login"))

    todo = Todo.query.filter_by(id=todo_id, user_id=session["user_id"]).first_or_404()
    if request.method == "POST":
        todo.title = request.form["title"]

        try:
            db.session.commit()
            flash("Task updated successfully!", "success")
            return redirect(url_for("index"))
        except Exception as e:
            flash(str(e), "danger")

    return render_template("update-task.html", todo=todo, title="Update Task")

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    if "user_id" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login"))

    todo = Todo.query.filter_by(id=todo_id, user_id=session["user_id"]).first_or_404()
    db.session.delete(todo)
    db.session.commit()

    flash("Task deleted successfully!", "success")
    return redirect(url_for("index"))


@app.route("/update_status/<int:todo_id>", methods=["POST"])
def update_status(todo_id):
    if "user_id" not in session:
        flash("Please log in to access this page.", "warning")
        return redirect(url_for("login"))

    todo = Todo.query.filter_by(id=todo_id, user_id=session["user_id"]).first_or_404()
    todo.done = bool(int(request.form["status"]))
    db.session.commit()

    flash("Task status updated successfully!", "success")
    return redirect(url_for("index"))

# Run the application
if __name__ == '__main__':
    app.run()
