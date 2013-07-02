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
#   along with this program.  If not, see <http://www.gnu.org/licenses/>

from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Blueprint
from flask.ext.babelex import gettext, ngettext
from flask.ext.login import LoginManager, login_user, logout_user, \
    current_user, login_required

from app.models import User, db_session
from app.forms.view import ViewForm 
from app import app
from app.lib import snapins


_ = gettext
edit_view_page = Blueprint('edit_view_page', __name__, static_folder='static', template_folder='templates')

@edit_view_page.route('/edit_view', methods=['GET', 'POST'])
@login_required
def edit_view():
    form = ViewForm() 
    #import ipdb;ipdb.set_trace()
    first = form.columns.append_entry()
    first.column.data='hoststate'
    form.columns.append_entry()
    if form.validate_on_submit():
        pass

    view_name = request.args.get('view_name', '')
    acknowledged = request.args.get('acknowledged', '')
    return snapins.render_sidebar_template('views/edit_view.html', acknowledged=acknowledged, view_name=view_name, form=form)
