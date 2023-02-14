from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class EncodeForm(FlaskForm):
    message = StringField("Message", validators=[DataRequired()])
    image = FileField("Image", validators=[FileRequired(), FileAllowed(["png"], "PNG image required.")])
    submit = SubmitField("Submit")


class DecodeForm(FlaskForm):
    image = FileField("Image", validators=[FileRequired(), FileAllowed(["png"], "PNG image required.")])
    submit = SubmitField("Submit")
