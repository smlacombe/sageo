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


from app.model.filters.filter import Filter
from app.model.filters.filter_text import FilterText
from app.model.filters.builtin import filters 

class FiltersManager():
    """ A sort of proxy that facilitates filters usage. There is one FiltersManager per view display.
    """   
    def __init__(self):
        self.__filters = {}

    def set_filters(self, filters):
        self.__filters = filters

    def get_filter_query(self):
        filter_query = ''
        for name, filter_value in self.__filters.get_filters().iteritems():
            if filter_value:
                filter_query = filter_query + filters[name].filter(filter_value)             

        return filter_query
    
    def get_filters_name(self):
        return filters.keys()
