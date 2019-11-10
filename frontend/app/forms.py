from flask_wtf import FlaskForm
from wtforms.fields import (IntegerField, StringField, SubmitField)
from wtforms.validators import InputRequired, Length
from wtforms.widgets import TextArea


class AddMusicForm(FlaskForm):
    lyrics = StringField('Insert Lyrics', widget=TextArea())

    submit = SubmitField('Submit')

    
