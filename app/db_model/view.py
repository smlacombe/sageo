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


filter_choices = [('off',_(u'Don''t use')),('hard',_(u"Hardcode")),('show',_(u"Show to user")), ('hide',_(u"Use for linking"))]
filter_choices_values = Enum('off','hard','show','hide')
#filter_column = Column(Enum(dict(filter_choices).keys()), info={'choices': filter_choices})
filter_column = Column(Enum('off','hard','show','hide'), info={'choices': filter_choices})
datasource_choices = [('hosts',_(u'All hosts')),('services',_(u"All services"))]

class View(Base):
    __tablename__ = 'views'
    id = Column(Integer, primary_key = True)
    title = Column(String(30), nullable=False, index = True, unique = True, info={'label':_(u'Title')})
    link_name = Column(String(30), nullable=False, unique=True, info={'label':_(u'Link name')})
    datasource = Column(Enum('hosts', 'services'), nullable=False, info={'choices': datasource_choices, 'label':_(u'Datasource')})
    buttontext = Column(String(15), info={'label':_(u'Button text')})
    reload_intervall = Column(SmallInteger, nullable=False, info={'label':_(u'Browser reload')}, default=30)
    hostname_option = Column(Enum('off','hard','show','hide'), nullable=False, info={'choices': filter_choices}, default='off')
    hostname_exact_match = Column(Boolean, default=False)
    hostname = Column(String(100))

    hoststate_option = Column(filter_choices_values, info={'choices': filter_choices}, default='off')
    hoststate_up = Column(Boolean, default=True)
    hoststate_down = Column(Boolean, default=True)
    hoststate_unreach = Column(Boolean, default=True)
    hoststate_pending = Column(Boolean, default=True)

    summary_option = Column(filter_choices_values, info={'choices': filter_choices}, default='off')
    summary = Column(Enum('yes', 'no', 'ignore'), default='no')
    #columns = relationship("ViewColumn")
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

    def get_filters(self):
        """
        Create a dictionnary of filters and their values
        """
        filters = {}  
        if not self.hostname_option == FILTER_OFF and self.hostname:
            if self.hostname_exact_match:
                filters[FILTER_EXACT_MATCH] = self.hostname 
            else:
                filters[FILTER_HOSTREGEX] = self.hostname
        if not self.hoststate_option == FILTER_OFF:
            value = {'UP':self.hoststate_up, 'DOWN':self.hoststate_down, 'UNREACH': self.hoststate_unreach, 'PENDING': self.hoststate_pending} 
            filters[FILTER_HOST_STATE] = value 
        if not self.summary_option == FILTER_OFF:
            filters[FILTER_IS_SUMMARY_HOST] = self.summary
        return filters

    def set_filters(self, filters):
        """
        Set class filter according filters dictionnary, almost of the time provening of url parameters.
        """
        for name, value in filters.items():
            if name == FILTER_EXACT_MATCH:
                if value:
                     self.hostname = value
                     self.hostname_exact_match = True
                else:
                     self.hostname_exact_match = False
            elif name == FILTER_HOSTREGEX: 
                self.hostname = value
            elif name == FILTER_HOST_STATE:
                import ipdb;ipdb.set_trace()
                if value['UP']:
                    if value['UP'] == 'True':
                         self.hoststate_up = True
                    else:
                         self.hoststate_up = False
                if value['DOWN']:
                    if value['DOWN'] == 'True': 
                        self.hoststate_down = True
                    else: 
                        self.hoststate_down = False
                if value['UNREACH']:
                    if value['UNREACH'] == 'True':
                        self.hoststate_unreach = True
                    else:
                         self.hoststate_unreach = False
                if value['PENDING']:
                    if value['PENDING'] == 'True': 
                        self.hoststate_pending = True
                    else:
                        self.hoststate_pending = False
            elif name == FILTER_IS_SUMMARY_HOST:
                self.summary = value
            
