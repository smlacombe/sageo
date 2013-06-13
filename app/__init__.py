#!/usr/bin/python
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__, static_folder="static")
app.config.from_object('config')
#app.config.from_envvar('FLASKR_SETTINGS', silent=False)
db = SQLAlchemy(app)
from app import sageo, controllers, models, lib
