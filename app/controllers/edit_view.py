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
from app.db_model.viewColumn import ViewColumn
from app.db_model.view import View
from app.db_model.viewFilters import ViewFilters
from app.managers.view_manager import ViewManager
from app.forms.view import ViewForm 
from app import app
from app.lib import snapins
from wtforms_components.validators import Unique
from app.model.columns.builtin import get_columns_pairs

_ = gettext
edit_view_page = Blueprint('edit_view_page', __name__, static_folder='static', template_folder='templates')
unique_validators= {}
@edit_view_page.route('/edit_view', methods=['GET', 'POST'])
@login_required
def edit_view():
    link_name = request.args.get('link_name', '')
    datasource = request.args.get('datasource', '')
    form = ViewForm(csrf_enabled=True)
    view_manager = ViewManager()
    
    if request.method=='GET':
        # Store the link_name parameter to use when we will be in post request
        session['link_name'] = link_name
        # We want to edit an existing view or create a new one?    
        if link_name:
            if view_manager.set_view(link_name): 
                view = view_manager.get_view()
                form = ViewForm(csrf_enabled=True, obj=view)
                form.populate_obj(view)
                form.set_columns_choices(view_manager.get_columns_choices())
                form.set_links_choices(view_manager.get_links_choices())
                columns = view_manager.get_columns() 
                groupers = view_manager.get_groupers()
                form.set_columns(columns)
                if groupers:
                    form.set_groupers(groupers)
                add_default_groupers(form)
                sorters = view_manager.get_sorters()
                if sorters:
                    form.set_sorters(sorters)
                add_default_sorters(form)

                filters = view_manager.get_filters()
                #form.populate_obj(filters)
            else:
                flash(_(u'View') + ' \'' + link_name + '\' ' +  _(u'doesn\'t exist'), 'error')
                return redirect('/view')
        else:
            if not datasource:
                datasource = 'hosts'
            view_manager.set_view_dummy(datasource) 
            view = view_manager.get_view()
            form = ViewForm(csrf_enabled=True, obj=view) 
            form.populate_obj(view)
            form.columns.append_entry()
            add_default_sorters(form)
            add_default_groupers(form)
            form.set_columns_choices(view_manager.get_columns_choices(), update=True)
            form.set_links_choices(view_manager.get_links_choices(), update=True)
    elif request.method=='POST':
        link_name = session['link_name']
        if link_name:
            saved_view = view_manager.set_view(link_name) 
            form = ViewForm(csrf_enabled=True, obj=saved_view)
            #form.populate_obj(saved_view)
        else:
            view_manager.set_view_dummy(datasource)

        form.set_links_choices(view_manager.get_links_choices(), update=True)
        
        if form.validate_on_submit():
            if not link_name:
                view = form.get_view()
                view_manager.add_view(view)
                link_name = view.link_name
                saved_view = view_manager.set_view(link_name) 
                view_manager.add_columns(form.get_columns(view.id))
                view_manager.add_sorters(form.get_sorters(view.id))
                view_manager.add_groupers(form.get_groupers(view.id))
                view_manager.add_filters(form.get_filters())
                db_session.commit()
            else:
                view = view_manager.set_view(link_name)   
                view_manager.update_view(form.get_view())
                view_manager.update_filters(form.get_filters())
                view_manager.add_columns(form.get_columns(view.id), delete_before=True) 
                view_manager.add_groupers(form.get_groupers(view.id), delete_before=True) 
                view_manager.add_sorters(form.get_sorters(view.id), delete_before=True)
            flash(_(u'View') + ' \'' + view_manager.get_view().title + '\' ' +  _(u'saved successfully!'), 'success')
            return redirect('/view?link_name='+ view_manager.get_view().link_name)

    filter_display = view_manager.get_filter_display(form.filters)
    return snapins.render_sidebar_template('views/edit_view.html', link_name=link_name, form=form, filter_display=filter_display)

def add_default_sorters(form):
    for x in range(0, app.config['MAX_SORTING_COLUMNS']-len(form.sorters)):
        form.sorters.append_entry()

def add_default_groupers(form):
    if len(form.groupers) == 0:
        form.groupers.append_entry()


