import copy
from flask.ext.login import UserMixin
from werkzeug.security import generate_password_hash, \
     check_password_hash
from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from flask.ext.babelex import lazy_gettext, gettext, ngettext, Babel
from app import babel, app
from flask import Flask
_ = lazy_gettext

db_engine = None
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False))

ROLE_USER = 0
ROLE_ADMIN = 1

def init_engine(db_uri):
    global db_engine
    db_engine = create_engine(db_uri)
    db_session.configure(bind=db_engine)

def init_db():
    Base.metadata.create_all(bind=db_engine)
    u1 = User(username='admin', language='en', email='admin@email.com', password='jobs', role=ROLE_ADMIN)
    u2 = User(username='susan', language='fr', email='john@email.com', password='jojo', role=ROLE_USER)
    db_session.add(u1)
    db_session.add(u2)
    db_session.commit()

def clear_db():
    Base.metadata.drop_all(bind=db_engine)

Base = declarative_base()
Base.query = db_session.query_property()

filter_choices = [('off',_(u'Don''t use')),('hard',_(u"Hardcode")),('show',_(u"Show to user")), ('hide',_(u"Use for linking"))]
#filter_column = Column(Enum(dict(filter_choices).keys()), info={'choices': filter_choices})
filter_column = Column(Enum('off','hard','show','hide'), info={'choices': filter_choices})
datasource_choices = [('allhost',_(u'All hosts')),('allservices',_(u"All services"))]
column_choices = [('hostname',_(u'Hostname')),('hoststate',_(u"Host state")), ('lastcheck',_(u"Last check"))]

class View(Base):
    __tablename__ = 'views'
    id = Column(Integer, primary_key = True)
    title = Column(String(30), index = True, unique = True, info={'label':_(u'Title')})
    link_name = Column(String(30), info={'label':_(u'Link name')}) 
    datasource = Column(Enum('allhost', 'allservices'), info={'choices': datasource_choices, 'label':_(u'Datasource')}) 
    buttontext = Column(String(15), info={'label':_(u'Button text')})
    reload_intervall = Column(SmallInteger, info={'label':_(u'Browser reload')})
    hostname_option = Column(Enum('off','hard','show','hide'), info={'choices': filter_choices}) 
    hostname_exact_match = Column(Boolean) 
    hostname = Column(String(100))

    hoststate_option = Column(Enum('off','hard','show','hide'), info={'choices': filter_choices})
    hoststate_up = Column(Boolean)
    hoststate_down = Column(Boolean)
    hoststate_unreach = Column(Boolean)
    hoststate_pending = Column(Boolean)

    summary_option = Column(Enum('off','hard','show','hide'), info={'choices': filter_choices})
    summary = Column(Enum('yes', 'no', 'ignore'))
    #columns = relationship("ViewColumn")
    layout_number_columns = Column(SmallInteger, info={'label':_(u'Number of columns')})

class ViewColumn(Base):
    __tablename__ = 'view_column'
    id = Column(Integer, primary_key=True)
    column = Column(Enum('hostname', 'hoststate', 'lastcheck'))
    parent_id = Column(Integer, ForeignKey(View.id)) 
    view = relationship(
        View,
        backref = 'View'    
    )

class User(UserMixin, Base):
    __tablename__ = 'users' 
    id = Column(Integer, primary_key = True)
    language = Column(String(2), unique = False)
    email = Column(String(120), index = True, unique = True)
    role = Column(SmallInteger, default = ROLE_USER)
    username = Column(String(120), index = True, unique = True)
    _password = Column('password', String(120),  unique = False) 

    def __init__(self, username, password, language, email, role):
        self.username = username
        self.set_password(password)
        self.language = language
        self.email = email
        self.role = role


    def _get_password(self):
        return self._password
    
    def set_password(self, password):
        self._password = generate_password_hash(password) 

    def check_password(self, password):
        return check_password_hash(self._password, password)

    def __repr__(self):
        return '<User %r>' % (self.username)
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

