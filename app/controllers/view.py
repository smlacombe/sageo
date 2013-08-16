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
    link_name = request.args.get('link_name', '')
    if link_name:
        form = ViewFiltersForm()
    else:
        form = ViewForm()

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
                query_param = dict([(k, v[0]) for k, v in query_param.items()])
                for name in filters_name:
                    arg = query_param.get(name, '')
                    if arg:
                        # TODO: find a better way to check if it is a dictionnary
                        if '{' in arg:
                            filters_url_values[name] = dict(ast.literal_eval(arg)) 
                        else:
                            filters_url_values[name] = arg

                if filters_url_values:
                    data_rows_manager.set_extra_filters(filters_url_values)

                arg = query_param.get('sort_by', '')
                if arg:
                    sort_by = dict(ast.literal_eval(arg))
                    data_rows_manager.set_extra_sorters(sort_by)
                    

                view = data_rows_manager.get_view()
                viewFilters = view_manager.get_filters() 
                form = ViewFiltersForm(obj=viewFilters)                   
                form.populate_obj(viewFilters)
                filter_display = view_manager.get_filter_display(form)
                return snapins.render_sidebar_template('views/view.html', controller=globals(), form=form, data_rows_manager=data_rows_manager, extra_filter = extra_filter, filter_display = filter_display)
            else:
                flash(_(u'View') + ' \'' + link_name + '\' ' +  _(u'doesn\'t exist'), 'error')
                return redirect('/view')
        else:
            views = View.query.all()
            return snapins.render_sidebar_template('views/view.html', views=views, form=form)

        return snapins.render_sidebar_template('views/view.html', link_name=link_name)
    elif request.method=='POST':
        if link_name:
            viewFilters = form.get_filters()
            return redirect(add_to_cur_url(request, viewFilters.get_filters()))
        else:
            datasource = form.datasource.data
            return redirect('/edit_view?datasource='+ datasource)

def get_sort_url(request, colname, orderAttr):
    url = urlparse.urlparse(request.url)
    query_param = urlparse.parse_qs(url.query)
    query_param = dict([(k, v[0]) for k, v in query_param.items()])
    arg = query_param.get('sort_by', '')
    if arg:
        sortBy = dict(ast.literal_eval(arg))       
    else:
        sortBy = {}
   
    if orderAttr == '1':
        order = '0'
    elif orderAttr == '0':
        order = '1'
    else:
        order = '0'

    sortBy[colname] = order
    dic = {'sort_by': sortBy} 
    return add_to_cur_url(request, dic) 

def add_to_cur_url(request, objs):
    url = urlparse.urlparse(request.url)
    query_param = urlparse.parse_qs(url.query)
    query_param = dict([(k, v[0]) for k, v in query_param.items()])
    for name, value in objs.items(): 
        query_param[name] = value
    param = urllib.urlencode(query_param)
    return request.base_url + '?' + param


