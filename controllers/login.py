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

_ = gettext
auth = Module(__name__)
sageo = current_app

@auth.route('/login', methods=['GET', 'POST'])
def login():
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

@auth.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash(_(u'You were logged out'))
    return redirect(url_for('show_entries'))
