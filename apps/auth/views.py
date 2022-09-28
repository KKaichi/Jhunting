from apps.app import db
from apps.auth.forms import LoginForm, SignUpForm
from apps.crud.models import User
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user

auth = Blueprint("auth", __name__, template_folder="templates", static_folder="static")


@auth.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignUpForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )

        if user.is_duplicate_email():
            flash("指定のメールアドレスは登録済みです．")
            return redirect(url_for("auth.signup"))

        db.session.add(user)
        db.session.commit()

        login_user(user)

        next_ = request.args.get("next")
        if next_ is None or not next_.startwith("/"):
            next_ = url_for("mypage.index")
        return redirect(next_)
    return render_template("auth/signup.html", form=form)


@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash("入力されたメールアドレスは登録されていません．")
            return render_template("auth/login.html", form=form)

        if user is not None and user.verify_password(form.password.data):
            login_user(user)
            return redirect(url_for("mypage.index"))
        flash("パスワードが違います．")
    return render_template("auth/login.html", form=form)


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home.index"))
