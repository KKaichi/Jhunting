from flask_wtf import FlaskForm
from wtforms import HiddenField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, InputRequired, length


class RequestResetForm(FlaskForm):
    email = StringField(
        "メールアドレス ",
        validators=[
            DataRequired(message="メールアドレスは必須です．"),
            Email(message="メールアドレスの形式で入力してください．"),
        ],
    )
    submit = SubmitField("メールを送信する")


class ResetPasswordForm(FlaskForm):
    token = HiddenField("token", validators=[InputRequired()])
    password = PasswordField(
        "パスワード (8文字以上20文字以内) : ",
        validators=[
            DataRequired(message="パスワードは必須です．"),
            length(8, 20, message="8文字以上20文字以内で入力してください．"),
        ],
    )
    confirm_password = PasswordField(
        "確認用パスワード : ",
        validators=[DataRequired(message="確認用パスワードは必須です．"), EqualTo("password")],
    )

    submit = SubmitField("変更する")
