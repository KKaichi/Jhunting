from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, length


class SignUpForm(FlaskForm):
    username = StringField(
        "ユーザ名 (15文字以内) : ",
        validators=[
            DataRequired(message="ユーザ名は必須です．"),
            length(1, 15, message="15文字以内で入力してください．"),
        ],
    )

    email = StringField(
        "メールアドレス : ",
        validators=[
            DataRequired(message="メールアドレスは必須です．"),
            Email(message="メールアドレスの形式で入力してください．"),
        ],
    )

    password = PasswordField(
        "パスワード (8文字以上20文字以内) : ",
        validators=[
            DataRequired(message="パスワードは必須です．"),
            length(8, 20, message="8文字以上20文字以内で入力してください．"),
        ],
    )
    confirm_password = PasswordField(
        "確認用パスワード : ",
        validators=[
            DataRequired(message="確認用パスワードは必須です．"),
            EqualTo("password", message="パスワードと確認用パスワードが異なります．"),
        ],
    )
    submit = SubmitField("新規登録")


class LoginForm(FlaskForm):
    email = StringField(
        "メールアドレス : ",
        validators=[
            DataRequired(message="メールアドレスを入力してください．"),
        ],
    )
    password = PasswordField(
        "パスワード : ",
        validators=[
            DataRequired(message="パスワードを入力してください．"),
        ],
    )

    submit = SubmitField("ログイン")
