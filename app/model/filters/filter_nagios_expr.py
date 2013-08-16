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
from sqlalchemy import *
from sqlalchemy.orm import *

class FilterNagiosExpr(Filter):
    def __init__(self, name, title, descr, pos_filter, neg_filter, default, column_names):
        Filter.__init__(self, name, title, descr)
        self.pos_filter = pos_filter
        self.neg_filter = neg_filter
        self.default = default
        self.column_names = column_names

    def filter(self, value):
        if value == 'yes':
            return self.pos_filter 
        else:
            return self.neg_filter 

    def get_col_def(self):
        return [Column(self.name, Enum('yes', 'no', 'ignore'), default=self.default)]

