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
import time
from flask.ext.babelex import format_timedelta
from flask.ext.babelex import format_datetime
from flask.ext.babelex import format_time
from datetime import datetime

class ColumnPainterLastEvent(ColumnPainter):
    """
    Column painter that print age for timestamp column like last_check
    """
    def get_readable(self, row):
        age = time.time() - row[self.name]
        return format_datetime(datetime.fromtimestamp(row[self.name])) 
