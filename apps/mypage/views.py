from datetime import datetime

from apps.account.models import UserImage
from apps.app import db
from apps.crud.models import User
from apps.mypage.forms import AddCompanyForm, AddEventForm
from flask import (
    Blueprint,
    current_app,
    redirect,
    render_template,
    send_from_directory,
    url_for,
)
from flask_login import current_user, login_required

mypage = Blueprint(
    "mypage", __name__, template_folder="templates", static_folder="static"
)


@mypage.route("/", methods=["GET", "POST"])
@login_required
def index():
    user_image = (
        db.session.query(User, UserImage)
        .join(UserImage)
        .filter(User.id == UserImage.user_id)
        .filter_by(user_id=current_user.id)
        .first()
    )
    date = datetime.today()
    company_form = AddCompanyForm()

    if company_form.validate_on_submit():
        return redirect(url_for("mypage.index"))

    return render_template(
        "mypage/index.html", user_image=user_image, form=company_form, date=date
    )


@mypage.route("/send/<path:filename>")
@login_required
def send(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)


@mypage.route("/add_event/<company_name>/<year_month_day>", methods=["GET", "POST"])
@login_required
def add_event(company_name, year_month_day):
    user_image = (
        db.session.query(User, UserImage)
        .join(UserImage)
        .filter(User.id == UserImage.user_id)
        .filter_by(user_id=current_user.id)
        .first()
    )
    year, month, day = year_month_day.split("-")
    month = "0" + month if (len(month) == 1) else month
    day = "0" + day if (len(day) == 1) else day

    form = AddEventForm()

    if form.validate_on_submit():
        return redirect(url_for("mypage.index"))

    return render_template(
        "mypage/add_event.html",
        user_image=user_image,
        form=form,
        company_name=company_name,
        year_month_day=year_month_day,
        year=year,
        month=month,
        day=day,
    )
