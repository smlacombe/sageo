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


from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.sqlalchemy import SQLAlchemy
from app import babel, app
from flask import Flask

db_engine = None
db = SQLAlchemy(app)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False))
Base = declarative_base()
Base.query = db_session.query_property()

from app.db_model.user import User, ROLE_ADMIN, ROLE_USER
from app.model.columns.builtin import get_columns_name
from app.db_model.viewColumn import ViewColumn
from app.db_model.view import View
from app.db_model.viewFilters import ViewFilters
from app.db_model.viewGrouper import ViewGrouper
from app.db_model.viewSorter import ViewSorter
from app.db_model.viewFilters import cache_columns

def init_engine(db_uri):
    global db_engine
    db_engine = create_engine(db_uri)
    db_session.configure(bind=db_engine)

def init_db():
    Base.metadata.create_all(bind=db_engine)
    create_default_users()
    create_default_views()

def create_default_users():
    u1 = User(username='admin', language='en', email='admin@email.com', password='jobs', role=ROLE_ADMIN)
    u2 = User(username='susan', language='fr', email='john@email.com', password='jojo', role=ROLE_USER)
    db_session.add(u1)
    db_session.add(u2)
    db_session.commit()

def create_default_views():

    #######################
    # All hosts view
    filters = ViewFilters()
    setattr(filters, 'host_regex_option', 'show')
    setattr(filters, 'host_option', 'show')
    setattr(filters, 'host_state_option', 'show')

    db_session.add(filters)
    db_session.commit()

    filters = ViewFilters.query.first()
    view = View()
    view.title = 'All hosts'
    view.link_name = 'allhosts'
    view.datasource = 'hosts'
    view.filters_id = filters.id
    view.layout_number_columns = 2
    db_session.add(view)
    db_session.commit()
    view = (View.query.filter_by(link_name=view.link_name).first())

    __add_column('last_check', view)
    __add_column('host_state', view)
    __add_column('host_name', view)

    #######################
    # All services view
    filters = ViewFilters()
    setattr(filters, 'host_regex_option', 'show')
    setattr(filters, 'host_option', 'show')
    setattr(filters, 'host_state_option', 'show')
    setattr(filters, 'service_state_option', 'show')

    db_session.add(filters)
    db_session.commit()

    filters = ViewFilters.query.all()[1]
    view = View()
    view.title = 'All services'
    view.link_name = 'allservices'
    view.datasource = 'services'
    view.layout_number_columns = 1
    view.filters_id = filters.id
    db_session.add(view)
    db_session.commit()

    __add_column('service_description', view)
    __add_column('service_state', view)

    ##########################
    # Host view
    filters = ViewFilters()
    setattr(filters, 'host_option', 'hide')
    setattr(filters, 'host_option', 'hide')

    db_session.add(filters)
    db_session.commit()

    filters = ViewFilters.query.all()[2]
    view = View()
    view.title = 'Host'
    view.link_name = 'host'
    view.datasource = 'hosts'
    view.layout_number_columns = 1
    view.basic_layout = 'single'
    view.filters_id = filters.id
    db_session.add(view)
    db_session.commit()

    # add all columns for a host
    for column in get_columns_name('hosts'): 
        if column:
            __add_column(column, view)

    ##########################
    # Service view
    filters = ViewFilters()
    setattr(filters, 'service_option', 'hide')
    setattr(filters, 'host_option', 'hide')

    db_session.add(filters)
    db_session.commit()

    filters = ViewFilters.query.all()[3]
    view = View()
    view.title = 'Service'
    view.link_name = 'service'
    view.datasource = 'services'
    view.layout_number_columns = 1
    view.basic_layout = 'single'
    view.filters_id = filters.id
    db_session.add(view)
    db_session.commit()

    # add all columns for a service
    for column in get_columns_name('services'):
        if column:
            __add_column(column, view)

    ##########################################
    # CRIT Services of host
    filters = ViewFilters()
    setattr(filters, 'service_state_option', 'hard')
    setattr(filters, 'service_state_ok', False)
    setattr(filters, 'service_state_warning', False)
    setattr(filters, 'service_state_critical', True)
    setattr(filters, 'service_state_unknown', False)

    setattr(filters, 'site_option', 'hide')
    setattr(filters, 'host_option', 'hide')

    db_session.add(filters)
    db_session.commit()

    filters = ViewFilters.query.all()[4]
    view = View()
    view.title = 'CRIT Services of host'
    view.link_name = 'host_crit'
    view.datasource = 'services'
    view.layout_number_columns = 2
    view.filters_id = filters.id
    db_session.add(view)
    db_session.commit()

    __add_column('service_state', view)
    __add_column('service_description', view)
    __add_column('service_plugin_output', view)
    __add_column('last_check', view) 

def __add_column(name, view):
    col = ViewColumn()
    col.column = name 
    col.parent_id = view.id
    db_session.add(col)
    db_session.commit()


def clear_db():
    Base.metadata.drop_all(bind=db_engine)

