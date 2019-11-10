from flask import redirect, render_template
from app import app
from .parser import make_presentation

from . import db
from .forms import AddMusicForm


@app.route("/", methods=['GET', 'POST'])
def index():
    form = AddMusicForm()
    if form.validate_on_submit():
        print(form.lyrics.data)
        URL = make_presentation(form.lyrics.data)
        
        return render_template('index.html', form=form, URL=URL)
    return render_template('index.html', form=form)
