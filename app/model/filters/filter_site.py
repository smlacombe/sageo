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


from .filter import Filter
from builtin import FILTER_SITE 
from sqlalchemy import *
from sqlalchemy.orm import *
from app import app

class FilterSite(Filter): 
    def __init__(self, name, title, descr): 
        Filter.__init__(self, name, title, descr) 
        self.column_names = ['site']
    def filter(self, site):
        '''
        Leave livestatus filter with the site with it internal function.
        '''
        return 'Sites: %s\n'% site

    def get_col_def(self):
        sites = []

        for site in app.config['SITES'].keys():
            sites.append(site)
        
        return [Column('site', Enum(*sites))]

