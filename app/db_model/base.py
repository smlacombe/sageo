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
    filters = ViewFilters()
    setattr(filters, 'host_regex_option', 'show')
    setattr(filters, 'host_option', 'show')
    setattr(filters, 'host_state_option', 'show')

    db_session.add(filters)
    db_session.commit()

    filters = ViewFilters.query.first()
    view1 = View()
    view1.title = 'All hosts'
    view1.link_name = 'allhosts'
    view1.datasource = 'hosts'
    view1.filters_id = filters.id
    view1.layout_number_columns = 2
    db_session.add(view1)
    db_session.commit()
    view1 = (View.query.filter_by(link_name=view1.link_name).first())

    col1 = ViewColumn()
    col1.column = 'host_name'
    col1.parent_id = view1.id
    db_session.add(col1)

    col2 = ViewColumn()
    col2.column = 'host_state'
    col2.parent_id = view1.id
    db_session.add(col2)

    col3 = ViewColumn()
    col3.column = 'last_check'
    col3.parent_id = view1.id
    db_session.add(col3)
    db_session.commit()

    sort1 = ViewSorter()
    sort1.column = 'host_name'
    sort1.sorter_option = '1'
    sort1.parent_id = view1.id
    db_session.add(sort1)
    db_session.commit()

    group1 = ViewGrouper()
    group1.column = 'site'
    group1.parent_id = view1.id
    db_session.add(group1)
    db_session.commit()


    filters = ViewFilters()
    setattr(filters, 'host_regex_option', 'show')
    setattr(filters, 'host_option', 'show')
    setattr(filters, 'host_state_option', 'show')
    setattr(filters, 'service_state_option', 'show')

    db_session.add(filters)
    db_session.commit()

    filters = ViewFilters.query.all()[1]
    view2 = View()
    view2.title = 'All services'
    view2.link_name = 'allservices'
    view2.datasource = 'services'
    view2.layout_number_columns = 1
    view2.filters_id = filters.id
    db_session.add(view2)
    db_session.commit()

    col4 = ViewColumn()
    col4.column = 'service_description'
    col4.parent_id = view2.id
    db_session.add(col4)
    db_session.commit()

    col5 = ViewColumn()
    col5.column = 'service_state'
    col5.parent_id = view2.id
    db_session.add(col5)
    db_session.commit()




def clear_db():
    Base.metadata.drop_all(bind=db_engine)

