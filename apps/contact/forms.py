from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired, length


class ContactForm(FlaskForm):
    discription = TextAreaField(
        "問い合わせ内容 (2000文字以内) : ",
        validators=[
            DataRequired(message="問い合わせ内容は必須です．"),
            length(1, 2000, message="2000文字以内で入力してください．"),
        ],
    )

    submit = SubmitField("送信")
