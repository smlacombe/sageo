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


from .column_painter import ColumnPainter

class ColumnPainterState(ColumnPainter):
    """
    Column painter that don't need value transformation to be human readable: Ex: host_name
    """

    def __init__(self, name, title, short_title, datasources, states):
        ColumnPainter.__init__(self, name, title, short_title, datasources)
        self.states = states

    def get_readable(self, row):
        return self.states[row[self.name]]
