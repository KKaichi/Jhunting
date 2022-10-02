from collections import defaultdict
from datetime import datetime

from apps.account.models import UserImage
from apps.app import db
from apps.crud.models import User
from apps.mypage.forms import AddCompanyForm, AddEventForm
from apps.mypage.models import Company, Event
from flask import (
    Blueprint,
    current_app,
    flash,
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
        company = Company(
            user_id=current_user.id,
            company_name=company_form.company_name.data,
        )
        if company.is_duplicate_company_name():
            flash("登録済みです．")
            return redirect(url_for("mypage.index"))

        db.session.add(company)
        db.session.commit()

        return redirect(url_for("mypage.index"))

    companise = Company.query.filter_by(user_id=current_user.id).all()
    if companise is not None:
        company_list = []
        company_event = [[] for i in range(len(companise))]
        for count in range(len(companise)):
            company_list.append(companise[count].company_name)
            events = Event.query.filter_by(
                user_id=current_user.id, company_id=companise[count].id
            ).all()
            for event in events:
                company_event[count].append(
                    [
                        event.event_name,
                        str(event.start_day),
                        str(event.start_time),
                        str(event.finish_day),
                        str(event.finish_time),
                        event.memo,
                    ]
                )
    if not company_list:
        company_list = 0

    return render_template(
        "mypage/index.html",
        user_image=user_image,
        form=company_form,
        date=date,
        company_event=company_event,
        company_list=company_list,
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
        company = Company.query.filter_by(
            user_id=current_user.id, company_name=company_name
        ).first()
        event = Event(
            user_id=current_user.id,
            company_id=company.id,
            event_name=form.event_type.data,
            start_day=form.start_date.data,
            start_time=form.start_time.data,
            finish_day=form.finish_date.data,
            finish_time=form.finish_time.data,
            memo=form.discription.data,
        )
        db.session.add(event)
        db.session.commit()

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
