from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, RadioField
from wtforms.validators import DataRequired, AnyOf


class EncodeForm(FlaskForm):
    message = StringField("Message", validators=[DataRequired()])
    image = FileField("Image", validators=[FileRequired(), FileAllowed(["png"], "PNG image required.")])
    consumed_bits = RadioField("How many bits per color channel to be used for encoding?",
                               choices=[("1", "1bpc"), ("2", "2bpc"), ("4", "4bpc")],
                               validators=[AnyOf(["1", "2", "4"], "Please choose one of the radio buttons.")])
    submit = SubmitField("Submit")


class DecodeForm(FlaskForm):
    image = FileField("Image", validators=[FileRequired(), FileAllowed(["png"], "PNG image required.")])
    consumed_bits = RadioField("How many bits per color channel were used during the encoding process?",
                               choices=[(1, "1bpc"), (2, "2bpc"), (4, "4bpc")],
                               validators=[AnyOf(["1", "2", "4"], "Please choose one of the radio buttons.")])
    submit = SubmitField("Submit")
