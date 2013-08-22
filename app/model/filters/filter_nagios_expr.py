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


from .filter_tristate import FilterTristate
from sqlalchemy import *
from sqlalchemy.orm import *

class FilterNagiosExpr(FilterTristate):
    def __init__(self, name, title, descr, default, column, pos_filter, neg_filter):
        FilterTristate.__init__(self, name, title, descr, default, column)
        self.pos_filter = pos_filter
        self.neg_filter = neg_filter

    def filter(self, value):
        if value == '1':
            return self.pos_filter 
        elif value == '0': 
            return self.neg_filter 
        else:
            return ""

