from flask import redirect, render_template
from app import app

from . import db
from .forms import AddMusicForm

@app.route("/", methods=['GET'])
def index():
    form = AddMusicForm()
    return render_template('index.html', form=form)






