#!/usr/bin/python
import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from app import controllers, lib, models
from models import User, init_engine, clear_db, init_db, db_session
from flask import request, session, g, redirect, url_for, \
    abort, render_template, flash
from flask.ext.login import LoginManager, login_user, logout_user, \
    current_user, login_required
from flaskext.babel import Babel
from controllers.login import login_page
from controllers.index import mod_main
from controllers.side import mod_side

app = Flask(__name__, static_folder="static")
app.config.from_object('config')
init_engine(app.config['SQLALCHEMY_DATABASE_URI'])
clear_db()
init_db()

login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.teardown_request
def remove_db_session(exception=None):
    db_session.remove()

babel = Babel(app)
@babel.localeselector
def get_locale():
    return 'fr'


@app.route('/images/<path:filename>')
def send_image(filename):
    return app.send_static_file("images/"+filename)

# Module
#import ipdb;ipdb.set_trace()
app.register_blueprint(login_page)
app.register_module(mod_main)
app.register_module(mod_side)

