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

class FilterText(Filter):
    def __init__(self, name, title, descr, column_names, operation):
        Filter.__init__(self, name, title, descr)
        self.operation = operation
        self.column_names = column_names

    def filter(self, column_value):
        if column_value:
             return "Filter: %s %s %s\n" % (self.column_names[0], self.operation, column_value)
        else:
            return ""

    def get_col_def(self):
        return [Column(self.name, String(100), info={'label':self.title})]
