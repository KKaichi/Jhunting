from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    RadioField,
    StringField,
    SubmitField,
    TextAreaField,
    TimeField,
)
from wtforms.validators import DataRequired


class AddEventForm(FlaskForm):

    event_type = RadioField(
        "イベント",
        choices=[
            "ES",
            "テスト",
            "GD",
            "面接",
            "面談",
            "セミナー",
            "OB訪問",
            "インターン",
        ],
    )

    start_date = DateField()
    start_time = TimeField()
    finish_date = DateField()
    finish_time = TimeField()

    discription = TextAreaField(
        "メモ",
    )

    submit = SubmitField("追加")


class AddCompanyForm(FlaskForm):

    company_name = StringField("会社名", validators=[DataRequired(message="ユーザ名は必須です．")])

    submit = SubmitField("登録")


class DeleteCompanyForm(FlaskForm):
    delete = SubmitField("削除")
