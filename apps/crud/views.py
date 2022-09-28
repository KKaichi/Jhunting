from apps.app import db
from apps.crud.forms import UserForm
from apps.crud.models import User
from flask import Blueprint, abort, redirect, render_template, url_for
from flask_login import current_user, login_required

crud = Blueprint(
    "crud",
    __name__,
    template_folder="templates",
    static_folder="static",
)


@crud.route("/")
@login_required
def index():
    if current_user.email != "kkaichi.sea.earth@gmail.com":
        return abort(400)
    return render_template("crud/index.html")


@crud.route("/sql")
@login_required
def sql():
    if current_user.email != "kkaichi.sea.earth@gmail.com":
        return abort(400)
    db.session.query(User).all()
    return "コンソールログを確認してください"


@crud.route("/users/new", methods=["GET", "POST"])
@login_required
def create_user():
    if current_user.email != "kkaichi.sea.earth@gmail.com":
        return abort(400)
    form = UserForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data,
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    return render_template("crud/create.html", form=form)


@crud.route("/users")
@login_required
def users():
    if current_user.email != "kkaichi.sea.earth@gmail.com":
        return abort(400)
    users = User.query.all()
    return render_template("crud/index.html", users=users)


@crud.route("/users/<user_id>", methods=["GET", "POST"])
@login_required
def edit_user(user_id):
    if current_user.email != "kkaichi.sea.earth@gmail.com":
        return abort(400)
    form = UserForm()

    user = User.query.filter_by(id=user_id).first()

    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("crud.users"))
    return render_template("crud/edit.html", user=user, form=form)


@crud.route("/users/<user_id>/delete", methods=["POST"])
@login_required
def delete_user(user_id):
    if current_user.email != "kkaichi.sea.earth@gmail.com":
        return abort(400)
    user = User.query.filter_by(id=user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("crud.users"))
