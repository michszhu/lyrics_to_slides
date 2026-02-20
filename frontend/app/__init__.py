"""
Initialize the Flask application
"""
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create database
db = SQLAlchemy()

# Initialize the application
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-in-production')

# Configure the application with database information
database_url = os.environ.get('DATABASE_URL', 'sqlite:///flask-data.db')
# Railway/Heroku use postgres:// but SQLAlchemy 1.4+ expects postgresql://
if database_url.startswith('postgres://'):
    database_url = 'postgresql://' + database_url[10:]
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Import the views/routes
from . import views
