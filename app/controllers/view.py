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

from app import app
from app.lib import snapins
from app.managers.data_rows_manager import DataRowsManager
from app.db_model.view import View
_ = gettext
view_page = Blueprint('view_page', __name__, static_folder='static', template_folder='templates')

@view_page.route('/view')
@login_required
def view():
    link_name = request.args.get('link_name', '')
    dataRowsManager = DataRowsManager() 
    if link_name:    
        if dataRowsManager.set_view(link_name):
            print dataRowsManager.get_rows()
        else:
            flash(_(u'View') + ' \'' + link_name + '\' ' +  _(u'doesn\'t exist'), 'error')
            return redirect('/view')
    else:
        views = View.query.all()
        return snapins.render_sidebar_template('views/view.html', views=views)

    return snapins.render_sidebar_template('views/view.html', link_name=link_name)
