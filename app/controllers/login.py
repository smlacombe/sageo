#   
#   Copyright (C) 2013 Savoir-Faire Linux Inc.
#   
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Module, current_app, Blueprint
from flask.ext.babelex import gettext, ngettext
from flask.ext.login import LoginManager, login_user, logout_user, \
    current_user, login_required

from app.models import User, db_session
from app.forms.login import LoginForm
from app.lib import auth
from app import babel, app

_ = gettext
login_page = Blueprint('login_page', __name__, static_folder='static', template_folder='templates')
sageo = Flask(__name__)

@login_page.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated():
        return redirect('/')

    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is not None and user.check_password(form.password.data):
            if login_user(user, remember=form.remember.data):
                # Enable session expiration only if user hasn't chosen to be
                # remembered.
                session.permanent = not form.remember.data
                flash(_('Logged in successfully!'), 'success')
                return redirect('/') 
            else:
                flash(_('This username is disabled!'), 'error')
        else:
            flash(_('Wrong username or password!'), 'error')
    return render_template('users/login.html', version='0.1', form=form) 

@login_page.route('/logout')
@login_required
def logout():
    logout_user()
    flash(_('You have logged out!'))
    return redirect('/') 
