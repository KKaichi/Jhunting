import uuid
from pathlib import Path

from apps.account.forms import UploadImageForm
from apps.account.models import UserImage
from apps.app import db
from apps.crud.models import User
from flask import Blueprint, current_app, render_template, send_from_directory
from flask_login import current_user, login_required

account = Blueprint(
    "account", __name__, template_folder="templates", static_folder="static"
)


@account.route("/", methods=["GET", "POST"])
@login_required
def index():
    upload_image_form = UploadImageForm()
    if upload_image_form.validate_on_submit():
        file = upload_image_form.image.data
        ext = Path(file.filename).suffix
        image_uuid_file_name = str(uuid.uuid4()) + ext

        image_path = Path(current_app.config["UPLOAD_FOLDER"], image_uuid_file_name)
        file.save(image_path)

        now_image = UserImage.query.filter_by(user_id=current_user.id).first()
        if now_image:
            db.session.delete(now_image)

        new_image = UserImage(user_id=current_user.id, image_path=image_uuid_file_name)
        db.session.add(new_image)
        db.session.commit()
    user_image = (
        db.session.query(User, UserImage)
        .join(UserImage)
        .filter(User.id == UserImage.user_id)
        .filter_by(user_id=current_user.id)
        .first()
    )
    return render_template(
        "account/index.html", form=upload_image_form, user_image=user_image
    )


@account.route("/send/<path:filename>")
@login_required
def send(filename):
    return send_from_directory(current_app.config["UPLOAD_FOLDER"], filename)
