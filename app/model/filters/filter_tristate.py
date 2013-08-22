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
from flask.ext.wtf import RadioField
from flask.ext.babelex import gettext, ngettext

_ = gettext

class FilterTristate(Filter):
    def __init__(self, name, title, descr, default, column):
        Filter.__init__(self, name, title, descr)
        self.default = default 
        self.column_names = column
        self.form_def = [RadioField(choices=[('1',_(u'Yes')),('0',_(u'No')),('-1',_(u'Ignore'))], default=default)] 

    def get_col_def(self):
        return [Column(self.name, Enum('1', '0', '-1'), default=self.default)]
