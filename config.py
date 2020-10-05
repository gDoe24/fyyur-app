import os
from flask import Flask
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


# TODO IMPLEMENT DATABASE URL

app=Flask(__name__)


app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://udacity:postgres@localhost:5432/fyyur'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
