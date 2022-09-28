from apps.account.models import UserImage
from apps.app import db
from apps.contact.forms import ContactForm
from apps.crud.models import User
from flask import Blueprint, current_app, flash, redirect, render_template, url_for
from flask_login import current_user, login_required
from flask_mail import Mail, Message

contact = Blueprint("contact", __name__, template_folder="templates")


@contact.route("/", methods=["GET", "POST"])
@login_required
def index():
    user_image = (
        db.session.query(User, UserImage)
        .join(UserImage)
        .filter(User.id == UserImage.user_id)
        .filter_by(user_id=current_user.id)
        .first()
    )

    form = ContactForm()

    if form.validate_on_submit():
        if not form.discription.data:
            flash("問い合わせ内容は必須です")
            return redirect(url_for("contact.index"))
        send_email(
            current_user.email,
            "問い合わせありがとうございました",
            "contact/contact_mail",
            username=current_user.username,
            description=form.discription.data,
        )
        send_email(
            "kkaichi.sea.earth@gmail.com",
            "問い合わせが届きました",
            "contact/contact_content",
            username=current_user.username,
            description=form.discription.data,
        )
        return redirect(
            url_for("contact.contact_complete", discription=form.discription.data)
        )
    return render_template("contact/index.html", form=form, user_image=user_image)


@contact.route("/contact_complete/<string:discription>")
def contact_complete(discription):
    user_image = (
        db.session.query(User, UserImage)
        .join(UserImage)
        .filter(User.id == UserImage.user_id)
        .filter_by(user_id=current_user.id)
        .first()
    )
    return render_template(
        "contact/contact_complete.html", discription=discription, user_image=user_image
    )


def send_email(to, subject, template, **kwargs):
    mail = Mail(current_app)
    msg = Message(
        subject,
        recipients=[to],
    )
    msg.body = render_template(template + ".txt", **kwargs)
    msg.html = render_template(template + ".html", **kwargs)
    mail.send(msg)
