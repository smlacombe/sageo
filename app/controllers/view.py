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
import urllib
import ast
import urlparse
from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash, Blueprint
from flask.ext.babelex import gettext, ngettext
from flask.ext.login import LoginManager, login_user, logout_user, \
    current_user, login_required

from app.forms.view import ViewForm
from app.forms.view import ViewFiltersForm
from app import app
from app.lib import snapins
from app.managers.data_rows_manager import DataRowsManager
from app.managers.view_manager import ViewManager
from app.db_model.view import View
_ = gettext
view_page = Blueprint('view_page', __name__, static_folder='static', template_folder='templates')

@view_page.route('/view', methods=['GET', 'POST'])
@login_required
def view():
    form = ViewFiltersForm()
    link_name = request.args.get('link_name', '')

    if request.method=='GET':
        data_rows_manager = DataRowsManager() 
        view_manager = ViewManager() 
        if link_name:    
            view_manager.set_view(link_name)

            if data_rows_manager.set_view(link_name):
                extra_filter = False
                # Get filters parameters if any
                filters_name = data_rows_manager.get_filters_name()
                filters_url_values = {}
                url = urlparse.urlparse(request.url)
                query_param = urlparse.parse_qs(url.query)
                for name in filters_name:
                    arg = query_param.get(name, '')
                    if arg:
                        # TODO: find a better way to check if it is a dictionnary
                        if '{' in arg[0]:
                            filters_url_values[name] = dict(ast.literal_eval(arg[0])) 
                        else:
                            filters_url_values[name] = arg[0]

                if filters_url_values:
                    data_rows_manager.set_extra_filters(filters_url_values)
                print data_rows_manager.get_rows()
                view = data_rows_manager.get_view()
                viewFilters = view_manager.get_filters() 
                form = ViewFiltersForm(obj=viewFilters)                   
                form.populate_obj(viewFilters)
                filter_display = view_manager.get_filter_display(form)
                return snapins.render_sidebar_template('views/view.html', form=form, data_rows_manager=data_rows_manager, extra_filter = extra_filter, filter_display = filter_display)
            else:
                flash(_(u'View') + ' \'' + link_name + '\' ' +  _(u'doesn\'t exist'), 'error')
                return redirect('/view')
        else:
            views = View.query.all()
            return snapins.render_sidebar_template('views/view.html', views=views)

        return snapins.render_sidebar_template('views/view.html', link_name=link_name)
    elif request.method=='POST':
        viewFilters = form.get_filters()
        url = urllib.urlencode(viewFilters.get_filters())
        return redirect('/view?link_name='+ link_name+'&'+ url)
