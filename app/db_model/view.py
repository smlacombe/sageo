from sqlalchemy import *
from sqlalchemy.orm import *
from app.db_model.base import Base
from app.db_model.viewFilters import ViewFilters
from flask.ext.babelex import lazy_gettext, gettext, ngettext, Babel
from app import babel, app
from flask import Flask

from app.model.filters.builtin import FILTER_HOSTREGEX
from app.model.filters.builtin import FILTER_EXACT_MATCH
from app.model.filters.builtin import FILTER_HOST_STATE
from app.model.filters.builtin import FILTER_IS_SUMMARY_HOST


_ = lazy_gettext

datasource_choices = [('hosts',_(u'All hosts')),('services',_(u"All services"))]

class View(Base):
    __tablename__ = 'views'
    id = Column(Integer, primary_key = True)
    title = Column(String(30), nullable=False, index = True, unique = True, info={'label':_(u'Title')})
    link_name = Column(String(30), nullable=False, unique=True, info={'label':_(u'Link name')})
    datasource = Column(Enum('hosts', 'services'), nullable=False, info={'choices': datasource_choices, 'label':_(u'Datasource')})
    buttontext = Column(String(15), info={'label':_(u'Button text')})
    reload_intervall = Column(SmallInteger, nullable=False, info={'label':_(u'Browser reload')}, default=30)
    layout_number_columns = Column(SmallInteger, nullable=False, info={'label':_(u'Number of columns')}, default=3)
    filters_id = Column(Integer, ForeignKey(ViewFilters.id))

    filters = relationship(
        ViewFilters,
        backref = 'view'
    )

    def update_view(self, view):
        del view._sa_instance_state 
        #self.__dict__.update(view.__dict__)
        for attribute, value in view.__dict__.iteritems():
            setattr(self, attribute, value)
        '''
        self.title = view.title
        self.link_name = view.link_name
        self.datasource = view.datasource
        self.buttontext = view.buttontext
        self.reload_intervall = view.reload_intervall
        self.layout_number_columns = view.layout_number_columns
        '''


