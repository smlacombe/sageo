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
from app.db_model.viewColumn import ViewColumn
from app.db_model.view import View

from app.forms.view import ViewForm 
from app import app
from app.lib import snapins
from wtforms_components.validators import Unique

_ = gettext
edit_view_page = Blueprint('edit_view_page', __name__, static_folder='static', template_folder='templates')
unique_validators= {}
@edit_view_page.route('/edit_view', methods=['GET', 'POST'])
@login_required
def edit_view():
    link_name = request.args.get('link_name', '')
    form = ViewForm(csrf_enabled=True)
    if request.method=='GET':
        # Store the link_name parameter to use when we will be in post request
        session['link_name'] = link_name
        # We wan't edit an existing view or create a new one?    
        if link_name:
            view = View.query.filter_by(link_name=link_name).first()    
            #import ipdb;ipdb.set_trace()                
            if view:
                form = ViewForm(csrf_enabled=True, obj=view)
                form.populate_obj(view)
                columns = ViewColumn.query.filter_by(parent_id=view.id).all()
                form.set_columns(columns)
            else:
                flash(_(u'View') + ' \'' + link_name + '\' ' +  _(u'doesn\'t exist'), 'error')
                return redirect('/view')
        else:
            col1 = ViewColumn() 
            form.populate_obj(col1) 
            form.columns.append_entry()
    elif request.method=='POST':
        link_name = session['link_name']
        if link_name:
            saved_view = View.query.filter_by(link_name=link_name).first()
            form = ViewForm(csrf_enabled=True, obj=saved_view)
            form.populate_obj(saved_view)
    
        if form.validate_on_submit():
           # import ipdb;ipdb.set_trace();
            if not link_name:
                view = form.get_view()
                db_session.add(view)
                db_session.commit() 
                saved_view = View.query.filter_by(title=view.title).first()
                add_form_columns(saved_view, form) 
                db_session.commit()
            else:
                view = View.query.filter_by(link_name=link_name).first()   
                view.update_view(form.get_view())
                columns = ViewColumn.query.filter_by(parent_id=view.id).all()

                # Delete all columns related to the view
                for column in columns:
                    db_session.delete(column)

                add_form_columns(view, form) 
                db_session.commit()
     
            flash(_(u'View') + ' \'' + view.title + '\' ' +  _(u'saved successfully!'), 'success')
            return redirect('/view')

    return snapins.render_sidebar_template('views/edit_view.html', acknowledged='', link_name=link_name, form=form)

def add_form_columns(view, form):
    columns = form.get_columns(view.id)
  #  import ipdb;ipdb.set_trace()
    for column in columns:
        db_session.add(column)

