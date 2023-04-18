from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class EncodeForm(FlaskForm):
    message = TextAreaField("Message", validators=[DataRequired("Message required.")])
    image = FileField(
        "Image",
        validators=[
            FileRequired("Image required."),
            FileAllowed(["png", "jpeg", "jpg"], "PNG or JPEG image required."),
        ],
    )
    submit = SubmitField("Submit")


class DecodeForm(FlaskForm):
    image = FileField(
        "Image",
        validators=[
            FileRequired("Image required."),
            FileAllowed(["png"], "PNG image required."),
        ],
    )
    seed = TextAreaField("Seed", validators=[DataRequired("Message required.")])
    submit = SubmitField("Submit")
