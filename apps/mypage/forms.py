from flask_wtf import FlaskForm
from wtforms import (
    DateField,
    RadioField,
    StringField,
    SubmitField,
    TextAreaField,
    TimeField,
)
from wtforms.validators import DataRequired, InputRequired

choices = [
    "ES",
    "テスト",
    "GD",
    "面接",
    "面談",
    "セミナー",
    "OB訪問",
    "インターン",
]


class AddEventForm(FlaskForm):

    event_type = RadioField("イベント", choices=choices)

    start_date = DateField()
    start_time = TimeField()
    finish_date = DateField()
    finish_time = TimeField()

    discription = TextAreaField(
        "メモ",
    )

    submit = SubmitField("追加")


class EditEventForm(FlaskForm):

    event_type = RadioField("編集イベント", choices=choices, default="ES")

    start_date = DateField()
    start_time = TimeField()
    finish_date = DateField()
    finish_time = TimeField()

    discription = TextAreaField(
        "メモ",
    )

    submit = SubmitField("変更")


class AddCompanyForm(FlaskForm):

    company_name = StringField("会社名", validators=[DataRequired(message="会社名は必須です．")])

    submit = SubmitField("登録")


class DeleteEventForm(FlaskForm):
    delete = SubmitField("削除")


class DeleteCompanyForm(FlaskForm):
    delete = SubmitField("削除")
