from flask import redirect, render_template
from app import app

from . import db
from .forms import AddMusicForm


@app.route("/", methods=['GET', 'POST'])
def index():
    form = AddMusicForm()
    if form.validate_on_submit():
        print(form.lyrics.data)
    return render_template('index.html', form=form)
