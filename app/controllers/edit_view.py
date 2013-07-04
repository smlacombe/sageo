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

from app.models import User, db_session, ViewColumn, View
from app.forms.view import ViewForm 
from app import app
from app.lib import snapins


_ = gettext
edit_view_page = Blueprint('edit_view_page', __name__, static_folder='static', template_folder='templates')

@edit_view_page.route('/edit_view', methods=['GET', 'POST'])
@login_required
def edit_view():
    form = ViewForm(csrf_enabled=True) 
    view_name = request.args.get('view_name', '')
#    import ipdb;ipdb.set_trace()
    if request.method=='GET':
        # Store the view_name parameter to use when we will be in post request
        session['view_name'] = view_name
        # We wan't edit an existing view or create a new one?    
        if view_name:
            view = View.query.filter_by(link_name=view_name).first()    
            #import ipdb;ipdb.set_trace()                
            if view:
                form.set_view(view)
                columns = ViewColumn.query.filter_by(parent_id=view.id).all()
                form.set_columns(columns)
            else:
                flash(_(u'View') + ' \'' + view_name + '\' ' +  _(u'doesn\'t exist'), 'error')
                return redirect('/')
        else:
            col1 = ViewColumn() 
            form.populate_obj(col1) 
            form.columns.append_entry()
    elif request.method=='POST':
        view_name = session['view_name']
        if view_name:
            saved_view = View.query.filter_by(link_name=view_name).first()
            # Workaround: remove unique validator to avoid raising validation error
            # the unique validator don't understand we are in editing mode...
            if form.title.data == saved_view.title:
                form.title.validators.pop()
            if form.link_name.data == saved_view.link_name:
                form.link_name.validators.pop()
    
        if form.validate_on_submit():
           # import ipdb;ipdb.set_trace();
            if not view_name:
                view = form.get_view()
                db_session.add(view)
                db_session.commit() 
                saved_view = View.query.filter_by(title=view.title).first()  
                columns = form.get_columns(saved_view.id)
     
                for column in columns:
                    db_session.add(column)

                db_session.commit()
                flash(_(u'View') + ' \'' + view.title + '\' ' +  _(u'saved successfully!'), 'success')
            else:
                view = View.query.filter_by(link_name=view_name).first()   
                view.update_view(form.get_view())
                db_session.commit()
     
            return redirect('/edit_view?view_name='+form.link_name.data)

    return snapins.render_sidebar_template('views/edit_view.html', acknowledged='', view_name=view_name, form=form)
