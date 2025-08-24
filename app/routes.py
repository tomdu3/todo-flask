from flask import flash, redirect, render_template, request, session, url_for
from .models import db, User, Todo
from sqlalchemy import or_

def register_routes(app):
    
    @app.route("/")
    def index():
        if "user_id" not in session:
            flash("Please log in to access this page.", "secondary")
            return redirect(url_for("login"))
        
        todos = Todo.query.filter_by(user_id=session["user_id"]).all()
        todos = sorted(todos, key=lambda x: x.created_at)
        return render_template("index.html", todos=todos, title="Home")

    @app.route("/login", methods=["GET", "POST"])
    def login():
        # check if the user is logged in
        if "user_id" in session:
            flash("You are already logged in.", "secondary")
            return redirect(url_for("index"))
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
            flash("Please log in to access this page.", "secondary")
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
            flash("Please log in to access this page.", "secondary")
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

    @app.route("/delete/<int:todo_id>")
    def delete(todo_id):
        if "user_id" not in session:
            flash("Please log in to access this page.", "secondary")
            return redirect(url_for("login"))

        todo = Todo.query.filter_by(id=todo_id, user_id=session["user_id"]).first_or_404()
        db.session.delete(todo)
        db.session.commit()

        flash("Task deleted successfully!", "success")
        return redirect(url_for("index"))

    @app.route("/update_status/<int:todo_id>", methods=["POST"])
    def update_status(todo_id):
        if "user_id" not in session:
            flash("Please log in to access this page.", "secondary")
            return redirect(url_for("login"))

        todo = Todo.query.filter_by(id=todo_id, user_id=session["user_id"]).first_or_404()
        todo.done = bool(int(request.form["status"]))
        db.session.commit()

        flash("Task status updated successfully!", "success")
        return redirect(url_for("index"))

    @app.context_processor
    def inject_user():
        """Injects the current user's username into all templates."""
        if "user_id" in session:
            user = User.query.get(session["user_id"])
            if user:
                return {'username': user.username}
        return {'username': None}
