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
from app.forms.acl.user_edit import UserEditForm
from app import app
from app.lib.auth import require, IsAdmin, Any, InGroups
from app.lib import snapins

_ = gettext
acl_page = Blueprint('acl_page', __name__, static_folder='static', template_folder='templates')

@acl_page.route('/acl/users', methods=['GET', 'POST'])
@login_required
@require(Any(IsAdmin(),InGroups()))
def users():
    users = User.query.all()

    return snapins.render_sidebar_template('acl/users.html', version='0.1', users=users)


@acl_page.route('/acl/user_edit/<int:user_id>', methods=['GET', 'POST'])
@acl_page.route('/acl/user_edit/', methods=['GET', 'POST'])
@login_required
def user_edit(user_id=None):
    form = UserEditForm()
    if user_id is None:
        # Create new user
        user = User()
    else:
        # Edit User
        user = User.query.get(user_id)
        if request.method=='GET':
            form.id.data = user.id
            form.username.data = user.username
            form.language.data = user.language
            form.email.data = user.email
            form.role.data = user.role
    # Post
    if request.method=='POST':
        if form.validate_on_submit():
            user.username = form.username.data
            user.language = form.language.data
            user.email = form.email.data
            user.role = form.role.data
            # Save password only if it's the same
            if form.password.data and user.id is not None:
                user.set_password(form.password.data)
            if user.id is None:
                # New user
                flash(_('User added successfully!'), 'success')
                db_session.add(user)
            else:
                flash(_('User edited successfully!'), 'success')
            db_session.commit()
            return redirect('/acl/users')

    return snapins.render_sidebar_template('acl/user_edit.html', version='0.1', form=form)

