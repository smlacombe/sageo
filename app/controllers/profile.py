#   
#   Copyright (C) 2013 Savoir-Faire Linux Inc.
#   
#   This file is part of Sageo
#   
#   Sageo is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Sageo is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Sageo.  If not, see <http://www.gnu.org/licenses/>

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Blueprint
from flask.ext.babelex import gettext, ngettext
from flask.ext.login import LoginManager, login_user, logout_user, \
    current_user, login_required

from app.db_model.base import db_session
from app.db_model.user import User
from app.forms.profile import ProfileForm
from app import app
from app.lib import snapins

_ = gettext
profile_page = Blueprint('profile_page', __name__, static_folder='static', template_folder='templates')

@profile_page.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = ProfileForm()
    
    if form.validate_on_submit():
        language = form.language.data
        password = form.password.data
        current_user.language = language 
        # Save password only if it's the same
        if password:
            current_user.set_password(password)
        db_session.commit()
        flash(_('Profile settings saved successfully!'), 'success')
        return redirect('/')
    else:
        form.language.data = current_user.language 
        
    return snapins.render_sidebar_template('users/profile.html', version='0.1', form=form)
