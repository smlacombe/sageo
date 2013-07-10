import os
from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask import request, session, g, redirect, url_for, \
    abort, render_template, flash
from flask.ext.login import LoginManager, login_user, logout_user, \
    current_user, login_required

from flask.ext.babelex import gettext, ngettext, Babel
_ = gettext


app = Flask(__name__, static_folder="static")
app.config.from_object('config')
babel = Babel(app)

from db_model.base import init_engine, clear_db, init_db, db_session
from app.db_model.user import User
login_manager = LoginManager()
login_manager.login_view = '/login'
login_manager.init_app(app)
login_manager.login_message = ""
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.teardown_request
def remove_db_session(exception=None):
    db_session.remove()

@babel.localeselector
def get_locale():
    if current_user.is_authenticated():
        return current_user.language 
    else:     
        return request.accept_languages.best_match([lang_code for lang_code in app.config['LANGUAGES']]) 

@app.route('/images/<path:filename>')
def send_image(filename):
    return app.send_static_file("images/"+filename)

from app import controllers, lib, db_model
from controllers.login import login_page
from controllers.index import index_page
from controllers.profile import profile_page
from controllers.frame import framed_page
from controllers.view import view_page
from controllers.edit_view import edit_view_page

init_engine(app.config['SQLALCHEMY_DATABASE_URI'])
clear_db()
init_db()


# Module
#import ipdb;ipdb.set_trace()
app.register_blueprint(login_page)
app.register_blueprint(index_page)
app.register_blueprint(profile_page)
app.register_blueprint(framed_page)
app.register_blueprint(edit_view_page)
app.register_blueprint(view_page)
