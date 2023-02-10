from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import DataRequired


class EncodeForm(FlaskForm):
    message = StringField("Message", validators=[DataRequired()])
    image = FileField("Image", validators=[DataRequired()])


class DecodeForm(FlaskForm):
    image = FileField("Image", validators=[DataRequired()])
