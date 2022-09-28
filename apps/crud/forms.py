from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, length


class UserForm(FlaskForm):
    username = StringField(
        "ユーザ名 (10文字以内)",
        validators=[
            DataRequired(message="ユーザ名は必須です．"),
            length(max=10, message="10文字以内で入力してください．"),
        ],
    )

    email = StringField(
        "メールアドレス ",
        validators=[
            DataRequired(message="メールアドレスは必須です．"),
            Email(message="メールアドレスの形式で入力してください．"),
        ],
    )

    password = PasswordField(
        "パスワード (8文字以上) ",
        validators=[
            DataRequired(message="パスワードは必須です．"),
            length(min=8, message="8文字以上入力してください．"),
            length(max=20, message="20文字以内で入力してください．"),
        ],
    )

    submit = SubmitField("新規登録")
