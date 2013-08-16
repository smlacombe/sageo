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


import abc

class ColumnPainter:
    """
    Base class for all column painters.
    A column painter provide informations on a specific column to be
    human readable.
    """
    __metaclass = abc.ABCMeta
    def __init__(self, name, title, short_title, datasources):
        self.name = name
        self.title = title
        self.short_title = short_title
        self.datasources = datasources
    
    @abc.abstractmethod
    def get_readable(self, row):
        """ return real col value """
