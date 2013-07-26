from sqlalchemy import *
from sqlalchemy.orm import *
from app.db_model.base import Base
from flask.ext.babelex import lazy_gettext, gettext, ngettext, Babel
from app import babel, app
from flask import Flask
from app.model.filters.builtin import filters
_ = lazy_gettext

filter_choices = [('off',_(u'Don''t use')),('hard',_(u"Hardcode")),('show',_(u"Show to user")), ('hide',_(u"Use for linking"))]
filter_choices_values = Enum('off','hard','show','hide')
cache_columns = {}

class ViewFilters(Base):
    __tablename__ = 'view_filters' 
    id = Column(Integer, primary_key=True)

    def get_filters(self):
        """
        Create a dictionnary of filters and their values
        """
        filters = {}
        for name, filt in filters.iteritems():
            if not getattr(self, name + '_option') == FILTER_OFF:
                cols = filt.get_col_def()
                if len(cols) > 1:
                    value_dict = {}
                    for col in filt.get_col_def():
                        value_dict[col.name] = getattr(self, col.name) 

                    filters[filt.name] = value_dict 
                else:
                    filters[filt.name] = getattr(self, col.name)

        return filters

    def set_filters(self, filters):
        """
        Set class filter according to filters dictionnary, almost of the time coming from url parameters.
        """
        for name, value in filters.iteritems():
            if not getattr(self, name + '_option') == FILTER_OFF:
                if type(value) == type(dict):
                    for sub_name, sub_value in value.iteritems():
                        setattr(self, sub_name, sub_value)
                else:
                    setattr(self, name, value) 
            
    def update(self, filters):
        del filters._sa_instance_state 
        for attribute, value in filters.__dict__.iteritems():
            setattr(self, attribute, value)


      
# Dynamically add columns to view_filters table
for name, filt in filters.iteritems():
    setattr(ViewFilters, name + '_option', Column(Enum('off','hard','show','hide'), nullable=False, info={'choices': filter_choices, 'label': filt.title}, default='off'))
    cache_columns[name + '_option'] = []
    for col in filt.get_col_def():
        cache_columns[name + '_option'].append(col.name)
        setattr(ViewFilters, col.name, col)   
