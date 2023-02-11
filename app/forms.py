from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField
from wtforms.validators import DataRequired


class EncodeForm(FlaskForm):
    message = StringField("Message", validators=[DataRequired()])
    image = FileField("Image", validators=[FileRequired(), FileAllowed(["jpg", "jpeg", "png"], "Image required.")])


class DecodeForm(FlaskForm):
    image = FileField("Image", validators=[FileRequired(), FileAllowed(["jpg", "jpeg", "png"], "Image required.")])
