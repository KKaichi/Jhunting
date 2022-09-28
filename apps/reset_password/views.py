from apps.app import db
from apps.crud.models import User
from apps.reset_password.forms import RequestResetForm, ResetPasswordForm
from flask import (
    Blueprint,
    abort,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_login import current_user
from flask_mail import Mail, Message

reset_password = Blueprint("reset_password", __name__, template_folder="templates")


@reset_password.route("/", methods=["GET", "POST"])
def index():
    form = RequestResetForm()
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            flash("入力されたメールアドレスは登録されていません．")
            return redirect(url_for("reset_password.index"))
        token = User.create_token(form.email.data)
        url = url_for("reset_password.new_password", token=token, _external=True)
        send_email(user, form.email.data, "パスワードの再設定", "reset_password/reset_mail", url)
        flash("パスワードの再設定用メールを送信しました．")
        return redirect(url_for("auth.login"))
    return render_template("reset_password/reset_request.html", form=form)


@reset_password.route("/reset_password", methods=["GET", "POST"])
def new_password():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    if request.method == "GET":
        try:
            token = request.args.get("token")
            mail_address = User.load_token(token)
        except Exception:
            return abort(400)

        form = ResetPasswordForm(token=token)

        return render_template(
            "reset_password/reset_password.html", form=form, mail_address=mail_address
        )

    else:
        form = ResetPasswordForm()
        try:
            mail_address = User.load_token(form.token.data)
        except Exception:
            return abort(400)
        if form.validate_on_submit():
            user = User.query.filter_by(email=mail_address).first()
            user.password = form.password.data
            db.session.add(user)
            db.session.commit()
            flash("パスワードを再設定しました．")
            return redirect(url_for("auth.login"))
        return render_template(
            "reset_password/reset_password.html", form=form, mail_address=mail_address
        )


def send_email(user, to, subject, template, url):
    mail = Mail(current_app)
    msg = Message(
        subject,
        recipients=[to],
    )
    msg.body = render_template(
        template + ".txt",
        user=user.username,
        url=url,
    )
    msg.html = render_template(
        template + ".html",
        user=user.username,
        url=url,
    )
    mail.send(msg)
