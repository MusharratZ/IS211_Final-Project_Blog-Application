from app.auth import bp
from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
    current_app,
)
from app.models.user import User
from app.extensions import db
from flask_login import login_user, current_user, login_required, logout_user
from .forms import LoginForm


@bp.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            email=request.form["email"],
            password=request.form["password"],
        )
        db.session.add(user)
        db.session.commit()
        return redirect(
            url_for(
                "index",
            )
        )
    return render_template("auth/register.html")


@bp.route("/login/", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        # If the user is already logged in, redirect them to the home page or another appropriate route
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        # Validate the user credentials
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)

            flash("Logged in successfully.")

            next_page = request.args.get("next")
            return redirect(next_page or url_for("index"))

        else:
            flash("Login failed. Please check your email and password.")

    return render_template("auth/login.html", form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
