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
from app.db_model.base import Base
from flask.ext.babelex import lazy_gettext, gettext, ngettext, Babel
from app import babel, app
from flask import Flask
from app.model.filters.builtin import filters
_ = lazy_gettext

FILTER_OFF = 'off'
FILTER_HARD = 'hard'
FILTER_SHOW = 'show'
FILTER_HIDE = 'hide'

filter_choices = [('off',_(u'Don''t use')),('hard',_(u"Hardcode")),('show',_(u"Show to user")), ('hide',_(u"Use for linking"))]
filter_choices_values = Enum('off','hard','show','hide')
cache_columns = {}

class ViewFilters(Base):
    __tablename__ = 'view_filters' 
    id = Column(Integer, primary_key=True)
    extra_filters = []

    def get_filters(self):
        """
        Create a dictionnary of filters and their values
        """
        filters_ret = {}
        for name, filt in filters.iteritems():
            option =  getattr(self, name + '_option')
            if option in [FILTER_SHOW, FILTER_HARD, FILTER_SHOW, FILTER_HIDE]:
                # If it is a hidden filters (linking), we consider it only if it come from an url
                if not option == FILTER_HIDE or name in self.extra_filters:
                    cols = filt.get_col_def()
                    if len(cols) > 1:
                        value_dict = {}
                        for col in filt.get_col_def():
                            value_dict[col.name] = getattr(self, col.name) 

                        filters_ret[filt.name] = value_dict 
                    else:
                        filters_ret[filt.name] = getattr(self, cols[0].name)
        return filters_ret

    def set_filters(self, filters):
        """
        Set class filter according to filters dictionnary, almost of the time coming from url parameters.
        """
        self.extra_filters = []
        for name, value in filters.iteritems():
            if not getattr(self, name + '_option') == FILTER_OFF:
                self.extra_filters.append(name)
                if type(value) == type(dict()):
                    for sub_name, sub_value in value.iteritems():
                        setattr(self, sub_name, sub_value)
                else:
                    setattr(self, name, value) 
            
    def update(self, filters):
        if hasattr(filters, '_sa_instance_state'):
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
