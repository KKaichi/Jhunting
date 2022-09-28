from flask_wtf.file import FileAllowed, FileField, FileRequired
from flask_wtf.form import FlaskForm
from wtforms.fields.simple import SubmitField


class UploadImageForm(FlaskForm):
    image = FileField(
        validators=[
            FileRequired("画像ファイル(png ,jpg, jpeg)を指定してください"),
            FileAllowed(
                ["png", "jpg", "jpeg"], "画像ファイルの形式は「png」 ,「jpg」, 「jpeg」のいずれかの形式のみです．"
            ),
        ]
    )
    submit = SubmitField("アップロード")
