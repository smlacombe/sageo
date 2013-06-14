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
    abort, render_template, flash, Module, current_app
from flaskext.babel import gettext, ngettext
from flask.ext.login import LoginManager, login_user, logout_user, \
    current_user, login_required

from app.models import User
from app.forms import LoginForm
from app import db
from app.lib import auth

_ = gettext
mod_auth = Module(__name__)
sageo = Flask(__name__)
#import ipdb;ipdb.set_trace()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(mod_auth)

@login_manager.user_loader
def load_user(user_id):
    import ipdb;ipdb.set_trace()
    return User.query.get(user_id)

@sageo.teardown_request
def remove_db_session(exception=None):
    db.session.remove()

@mod_auth.route('/login', methods=['GET', 'POST'])
def login():
    import ipdb;ipdb.set_trace()
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
                flash('Logged in successfully!', 'success')
                return redirect('/') 
            else:
                flash('This username is disabled!', 'error')
        else:
            flash('Wrong username or password!', 'error')
    return render_template('users/login.html', version='0.1', form=form) 


@mod_auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out!')
    return redirect('/') 

"""
    error = None
    if request.method == 'POST':
  #      import pdb;pdb.set_trace()
        if request.form['_username'] == '' or request.form['_password'] == '':
            error = _(u'no credentials entered')
        elif request.form['_username'] != sageo.config['USERNAME']:
            error = _(u'invalid username')
        elif request.form['_password'] != sageo.config['PASSWORD']:
            error = _(u'invalid password')
        else:
#            import ipdb;ipdb.set_trace() 
            session['username'] = request.form['_username'] 
            session['logged_in'] = True
            flash(_(u'You were logged in'))
            return redirect('/')
    return render_template('users/login.html', version='0.1',error=error)

@mod_auth.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash(_(u'You were logged out'))
    return redirect(url_for('show_entries'))
"""
