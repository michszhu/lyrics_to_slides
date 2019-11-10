from flask_wtf import FlaskForm
from wtforms.fields import (IntegerField, StringField, SubmitField)
from wtforms.validators import InputRequired, Length


class AddMusicForm(FlaskForm):
    lyrics = StringField('Insert Lyrics')

    submit = SubmitField('Submit')
