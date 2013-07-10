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

from app.db_model.base import db_session
from app.db_model.user import User
from app.db_model.view import View
from app.db_model.viewColumn import ViewColumn
from app import app
from app.lib import snapins
from app.lib import livestatus_query
_ = gettext
view_page = Blueprint('view_page', __name__, static_folder='static', template_folder='templates')

@view_page.route('/view')
@login_required
def view():
    view_name = request.args.get('view_name', '')
    if view_name:    
        view = View.query.filter_by(link_name=view_name).first()
        if view:
            columns = ViewColumn.query.filter_by(parent_id=view.id).all()
            rows = livestatus_query.get_rows(view, columns)
        else:
            flash(_(u'View') + ' \'' + view_name + '\' ' +  _(u'doesn\'t exist'), 'error')
            return redirect('/view')
    else:
        views = View.query.all()
        return snapins.render_sidebar_template('views/view.html', views=views)

    return snapins.render_sidebar_template('views/view.html', view_name=view_name)


 
