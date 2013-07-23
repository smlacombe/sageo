from sqlalchemy import *
from sqlalchemy.orm import *
from app.db_model.base import Base
from flask.ext.babelex import lazy_gettext, gettext, ngettext, Babel
from app import babel, app
from flask import Flask

from app.model.filters.builtin import FILTER_HOSTREGEX
from app.model.filters.builtin import FILTER_EXACT_MATCH
from app.model.filters.builtin import FILTER_HOST_STATE
from app.model.filters.builtin import FILTER_IS_SUMMARY_HOST


_ = lazy_gettext

FILTER_OFF = 'off'
FILTER_HARD = 'hard'
FILTER_SHOW = 'show'
FILTER_HIDE = 'hide'

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

    def update_view(self, view):
        self.title = view.title
        self.link_name = view.link_name
        self.datasource = view.datasource
        self.buttontext = view.buttontext
        self.reload_intervall = view.reload_intervall
        self.hostname_option = view.hostname_option
        self.hostname_exact_match = view.hostname_exact_match
        self.hostname = view.hostname
        self.hoststate_option = view.hoststate_option
        self.hoststate_up = view.hoststate_up
        self.hoststate_down = view.hoststate_down
        self.hoststate_unreach = view.hoststate_unreach
        self.hoststate_pending = view.hoststate_pending
        self.summary_option = view.summary_option
        self.summary = view.summary
        self.layout_number_columns = view.layout_number_columns

